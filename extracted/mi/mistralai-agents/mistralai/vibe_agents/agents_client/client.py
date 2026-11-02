from http import HTTPMethod
from urllib.parse import quote
from uuid import UUID

from mistralai.vibe_agents._http import _InternalHTTPClient
from mistralai.vibe_agents.agents_client._registration import _register_agent
from mistralai.vibe_agents.agents_client.api_models import (
    AgentDetailResponse,
    AgentResponse,
    ConnectorInput,
    ConnectorSelectionInput,
    CreateManagedAgentRequest,
    HarnessConfigInput,
    ListAgentsResponse,
    ManagedAgentResponse,
    PlainMCPServerInput,
    RegisterAgentRequest,
    SandboxConfigInput,
    SecretBindingInput,
    SessionInputSchemas,
    SkillInput,
)
from mistralai.vibe_agents.session_workflow.inputs import SubagentPolicy


class AgentsClient(_InternalHTTPClient):
    """Client for the Agents API."""

    async def create_managed_agent(
        self,
        *,
        agent_name: str,
        workflow_name: str,
        github_url: str,
        revision: str | None = None,
        working_dir: str | None = None,
        dockerfile_path: str | None = None,
        is_hardened: bool = True,
        description: str | None = None,
        harness_config: HarnessConfigInput | None = None,
        skills: list[SkillInput] | None = None,
        connectors: list[ConnectorInput] | None = None,
        secret_bindings: list[SecretBindingInput] | None = None,
        connector_selection: ConnectorSelectionInput | None = None,
        required_session_inputs: SessionInputSchemas | None = None,
        default_subagent_policy: SubagentPolicy | None = None,
        sandbox_config: SandboxConfigInput | None = None,
        mcp_servers: list[PlainMCPServerInput] | None = None,
    ) -> ManagedAgentResponse:
        body = CreateManagedAgentRequest(
            agent_name=agent_name,
            workflow_name=workflow_name,
            github_url=github_url,
            revision=revision,
            working_dir=working_dir,
            dockerfile_path=dockerfile_path,
            is_hardened=is_hardened,
            description=description,
            harness_config=harness_config,
            skills=skills or [],
            connectors=connectors or [],
            secret_bindings=secret_bindings or [],
            connector_selection=connector_selection,
            required_session_inputs=required_session_inputs,
            default_subagent_policy=default_subagent_policy,
            sandbox_config=sandbox_config,
            mcp_servers=mcp_servers or [],
        )
        response = await self.make_request(
            HTTPMethod.POST,
            "/agents",
            json=body.model_dump(mode="json"),
        )
        response.raise_for_status()
        return ManagedAgentResponse.model_validate(response.json())

    async def get_agent(self, agent_id: UUID) -> AgentDetailResponse:
        response = await self.make_request(HTTPMethod.GET, f"/agents/{agent_id}")
        response.raise_for_status()
        return AgentDetailResponse.model_validate(response.json())

    async def get_agent_by_name(self, agent_name: str) -> AgentDetailResponse:
        """Resolve an agent by the name a human types, whatever page it would list on."""
        response = await self.make_request(HTTPMethod.GET, f"/agents/by-name/{quote(agent_name, safe='')}")
        response.raise_for_status()
        return AgentDetailResponse.model_validate(response.json())

    async def list_agents(self, *, limit: int = 200, cursor: str | None = None) -> ListAgentsResponse:
        """One page of the agents this API key's workspace can reach, built-in ones included."""
        params: dict[str, str | int] = {"limit": limit}
        if cursor is not None:
            params["cursor"] = cursor
        response = await self.make_request(HTTPMethod.GET, "/agents", params=params)
        response.raise_for_status()
        return ListAgentsResponse.model_validate(response.json())

    async def shutdown_agent(self, agent_id: UUID) -> None:
        """Shut an agent down permanently, whether it is deployed or self-hosted.

        A deployed agent also loses its managed deployment. A self-hosted worker keeps
        running until its operator stops it; only its catalog binding is removed.
        """
        response = await self.make_request(HTTPMethod.DELETE, f"/agents/{agent_id}")
        response.raise_for_status()

    async def delete_managed_agent(self, agent_id: UUID) -> None:
        """Deprecated alias for :meth:`shutdown_agent`, which also covers self-hosted agents."""
        await self.shutdown_agent(agent_id)

    async def register_agent(
        self,
        *,
        agent_name: str,
        workflow_name: str,
        deployment_name: str | None = None,
        required_session_inputs: SessionInputSchemas | None = None,
        default_subagent_policy: SubagentPolicy | None = None,
        description: str | None = None,
        harness_config: HarnessConfigInput | None = None,
        sandbox_config: SandboxConfigInput | None = None,
        skills: list[SkillInput] | None = None,
        connectors: list[ConnectorInput] | None = None,
        connector_selection: ConnectorSelectionInput | None = None,
        mcp_servers: list[PlainMCPServerInput] | None = None,
        makes_own_sandbox: bool = False,
    ) -> AgentResponse:
        return await _register_agent(
            self,
            RegisterAgentRequest(
                agent_name=agent_name,
                workflow_name=workflow_name,
                deployment_name=deployment_name,
                required_session_inputs=required_session_inputs,
                default_subagent_policy=default_subagent_policy,
                description=description,
                harness_config=harness_config,
                sandbox_config=sandbox_config,
                skills=skills or [],
                connectors=connectors or [],
                connector_selection=connector_selection,
                mcp_servers=mcp_servers or [],
                makes_own_sandbox=makes_own_sandbox,
            ),
        )
