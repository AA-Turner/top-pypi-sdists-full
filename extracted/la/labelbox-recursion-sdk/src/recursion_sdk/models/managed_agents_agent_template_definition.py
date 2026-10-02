from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_agent_template_definition_mcp_servers_item import ManagedAgentsAgentTemplateDefinitionMcpServersItem
  from ..models.managed_agents_agent_template_definition_metadata import ManagedAgentsAgentTemplateDefinitionMetadata
  from ..models.managed_agents_agent_template_definition_multiagent import ManagedAgentsAgentTemplateDefinitionMultiagent
  from ..models.managed_agents_agent_template_definition_skills_item import ManagedAgentsAgentTemplateDefinitionSkillsItem
  from ..models.managed_agents_agent_template_definition_tools_item import ManagedAgentsAgentTemplateDefinitionToolsItem
  from ..models.managed_agents_agent_template_definition_toolsets_item import ManagedAgentsAgentTemplateDefinitionToolsetsItem
  from ..models.managed_agents_built_in_integration import ManagedAgentsBuiltInIntegration
  from ..models.managed_agents_inference_config import ManagedAgentsInferenceConfig
  from ..models.managed_agents_native_integration import ManagedAgentsNativeIntegration
  from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef





T = TypeVar("T", bound="ManagedAgentsAgentTemplateDefinition")



@_attrs_define
class ManagedAgentsAgentTemplateDefinition:
    """ Request body for creating an agent: its system prompt, model, tool surface, and default vault grants. Sessions
    snapshot the agent version at start, so later edits do not change a running session.

        Example:
            {'built_in_integrations': [{'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'tools': ['example']}],
                'default_credential_refs': [{'credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'default_project_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'default_rubric': 'example', 'default_vault_ids': ['example'], 'description': 'example',
                'disabled_integration_mcp_providers': ['example'], 'max_concurrent_sessions': 1, 'mcp_servers': [{'key':
                'example'}], 'metadata': {'key': 'example'}, 'model': 'example', 'model_config': {'max_tokens': 1,
                'provider_params': {'key': 'example'}, 'reasoning_effort': 'example', 'temperature': 1.5, 'top_p': 1.5},
                'multiagent': {'key': 'example'}, 'name': 'example-name', 'nativeIntegrations': [{'connectionId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'permission': 'example', 'resources': ['example']}], 'skills': [{'key':
                'example'}], 'system': 'example', 'toolsets': [{'type': 'evaluation'}], 'web_search_enabled': True}

        Attributes:
            model (str): Gateway model id, copied verbatim from the gateway models catalog (e.g. anthropic/claude-
                sonnet-4-5). Stored and returned prefixed as litellm:anthropic/claude-sonnet-4-5. An id the gateway does not
                serve is rejected with the list of ids that are.
            model_config (ManagedAgentsInferenceConfig): Sampling and generation settings for a model call, mirroring the
                provider's own request parameters. Set it on an agent or a session to govern every turn, and read it back on a
                model event to see what the call actually used. Example: {'max_tokens': 1, 'provider_params': {'key':
                'example'}, 'reasoning_effort': 'example', 'temperature': 1.5, 'top_p': 1.5}.
            name (str): Human-readable label for the agent. Required.
            system (str): System prompt for the agent.
            built_in_integrations (list[ManagedAgentsBuiltInIntegration] | Unset): Vendor integrations this agent may use,
                each naming an active organization connection an admin configured on the Integrations page (provider merge).
                Sessions receive a short-lived credential restricted to exactly those vendors and each connection's admin tool
                allow-list, delivered to the sandbox for the merge CLI; nothing is granted through a vault. Omit or send [] for
                none. Carried in full on every version write.
            default_credential_refs (list[ManagedAgentsVaultCredentialRef] | Unset): Individual default items within
                default_vault_ids. The list is a whitelist across every default vault, not a filter within one, so it must name
                every item the agent should receive. Omit to select every current item; [] alongside a non-empty
                default_vault_ids is rejected because it would select none.
            default_project_id (str | Unset): Labelbox project copied into sessions started from this agent when their
                create request omits project_id. A non-empty session project_id overrides it.
            default_rubric (str | Unset): Markdown rubric that sessions started from this agent are graded against when
                their create request omits an outcome. Must contain at least one gradeable criterion, written as markdown list
                items. A session that supplies its own outcome ignores this entirely.
            default_vault_ids (list[str] | Unset): Vaults granted by default when a session create request omits vault_ids.
                default_credential_refs may narrow their items.
            description (str | Unset): Optional free-text note about what the agent is for. Not sent to the model.
            disabled_integration_mcp_providers (list[str] | Unset): Native integration providers whose MCP tools sessions of
                this agent do not receive even though the grant is present. The grant still authenticates the provider's sandbox
                tools where it has any (git and gh for GitHub); the agent's own mcp_servers are never affected. Omission differs
                by operation: on createAgent it defaults to ["github"] (new agents use gh and git in the sandbox); on
                createAgentVersion it means none, as for every other field there; send [] to receive every provider's MCP tools.
            max_concurrent_sessions (int | Unset): Maximum number of this agent's root sessions that may run or wait on
                compute at once. Omit for unlimited. Sessions beyond the cap are accepted with execution_state=queued and wait
                until a slot frees.
            mcp_servers (list[ManagedAgentsAgentTemplateDefinitionMcpServersItem] | Unset): Remote MCP servers whose tools
                are added to the agent's tool surface. Each entry is an object with name and url, e.g. {"name": "docs", "url":
                "https://example.com/mcp"}. Credentials come from the vaults granted to the session, and the discovered tool
                list is snapshotted at session start, so a later edit here does not change a running session.
            metadata (ManagedAgentsAgentTemplateDefinitionMetadata | Unset): Free-form caller-owned JSON stored with the
                agent and returned on reads. Not interpreted by the service and never sent to the model.
            multiagent (ManagedAgentsAgentTemplateDefinitionMultiagent | Unset): Multiagent roster: the delegation targets
                this agent may hand work to, an optional advisor entry, and the interventionist posture. Snapshotted at session
                start; a child roster may tighten the recursion depth ceiling, never widen it.
            native_integrations (list[ManagedAgentsNativeIntegration] | Unset): Native connections this agent may use, with
                provider-enforced permission and resource restrictions. Omit or send [] for none. Stored in full on each agent
                version; secrets remain on the connection.
            skills (list[ManagedAgentsAgentTemplateDefinitionSkillsItem] | Unset): Skill declarations made available to the
                agent, passed through as given and snapshotted into the session at start. Capped at the 100 skills a session can
                carry.
            tools (list[ManagedAgentsAgentTemplateDefinitionToolsItem] | Unset): Deprecated alias for toolsets; accepts only
                the bare evaluation marker.
            toolsets (list[ManagedAgentsAgentTemplateDefinitionToolsetsItem] | Unset): Only the bare {type: evaluation}
                marker is supported, for evaluator agents. Omit or send [] for ordinary agents; built-in sandbox tools, MCP
                servers, and skills do not require a toolset. The tools field is a deprecated alias.
            web_search_enabled (bool | Unset): Whether sessions started from this agent may use the native web_search tool.
                Omit to enable it. The setting is snapshotted when a session starts. Default: True.
     """

    model: str
    model_config: ManagedAgentsInferenceConfig
    name: str
    system: str
    built_in_integrations: list[ManagedAgentsBuiltInIntegration] | Unset = UNSET
    default_credential_refs: list[ManagedAgentsVaultCredentialRef] | Unset = UNSET
    default_project_id: str | Unset = UNSET
    default_rubric: str | Unset = UNSET
    default_vault_ids: list[str] | Unset = UNSET
    description: str | Unset = UNSET
    disabled_integration_mcp_providers: list[str] | Unset = UNSET
    max_concurrent_sessions: int | Unset = UNSET
    mcp_servers: list[ManagedAgentsAgentTemplateDefinitionMcpServersItem] | Unset = UNSET
    metadata: ManagedAgentsAgentTemplateDefinitionMetadata | Unset = UNSET
    multiagent: ManagedAgentsAgentTemplateDefinitionMultiagent | Unset = UNSET
    native_integrations: list[ManagedAgentsNativeIntegration] | Unset = UNSET
    skills: list[ManagedAgentsAgentTemplateDefinitionSkillsItem] | Unset = UNSET
    tools: list[ManagedAgentsAgentTemplateDefinitionToolsItem] | Unset = UNSET
    toolsets: list[ManagedAgentsAgentTemplateDefinitionToolsetsItem] | Unset = UNSET
    web_search_enabled: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_agent_template_definition_mcp_servers_item import ManagedAgentsAgentTemplateDefinitionMcpServersItem # noqa: PLC0415
        from ..models.managed_agents_agent_template_definition_metadata import ManagedAgentsAgentTemplateDefinitionMetadata # noqa: PLC0415
        from ..models.managed_agents_agent_template_definition_multiagent import ManagedAgentsAgentTemplateDefinitionMultiagent # noqa: PLC0415
        from ..models.managed_agents_agent_template_definition_skills_item import ManagedAgentsAgentTemplateDefinitionSkillsItem # noqa: PLC0415
        from ..models.managed_agents_agent_template_definition_tools_item import ManagedAgentsAgentTemplateDefinitionToolsItem # noqa: PLC0415
        from ..models.managed_agents_agent_template_definition_toolsets_item import ManagedAgentsAgentTemplateDefinitionToolsetsItem # noqa: PLC0415
        from ..models.managed_agents_built_in_integration import ManagedAgentsBuiltInIntegration # noqa: PLC0415
        from ..models.managed_agents_inference_config import ManagedAgentsInferenceConfig # noqa: PLC0415
        from ..models.managed_agents_native_integration import ManagedAgentsNativeIntegration # noqa: PLC0415
        from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef # noqa: PLC0415
        model = self.model

        model_config = self.model_config.to_dict()

        name = self.name

        system = self.system

        built_in_integrations: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.built_in_integrations, Unset):
            built_in_integrations = []
            for built_in_integrations_item_data in self.built_in_integrations:
                built_in_integrations_item = built_in_integrations_item_data.to_dict()
                built_in_integrations.append(built_in_integrations_item)



        default_credential_refs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.default_credential_refs, Unset):
            default_credential_refs = []
            for default_credential_refs_item_data in self.default_credential_refs:
                default_credential_refs_item = default_credential_refs_item_data.to_dict()
                default_credential_refs.append(default_credential_refs_item)



        default_project_id = self.default_project_id

        default_rubric = self.default_rubric

        default_vault_ids: list[str] | Unset = UNSET
        if not isinstance(self.default_vault_ids, Unset):
            default_vault_ids = self.default_vault_ids



        description = self.description

        disabled_integration_mcp_providers: list[str] | Unset = UNSET
        if not isinstance(self.disabled_integration_mcp_providers, Unset):
            disabled_integration_mcp_providers = self.disabled_integration_mcp_providers



        max_concurrent_sessions = self.max_concurrent_sessions

        mcp_servers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.mcp_servers, Unset):
            mcp_servers = []
            for mcp_servers_item_data in self.mcp_servers:
                mcp_servers_item = mcp_servers_item_data.to_dict()
                mcp_servers.append(mcp_servers_item)



        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        multiagent: dict[str, Any] | Unset = UNSET
        if not isinstance(self.multiagent, Unset):
            multiagent = self.multiagent.to_dict()

        native_integrations: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.native_integrations, Unset):
            native_integrations = []
            for native_integrations_item_data in self.native_integrations:
                native_integrations_item = native_integrations_item_data.to_dict()
                native_integrations.append(native_integrations_item)



        skills: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.skills, Unset):
            skills = []
            for skills_item_data in self.skills:
                skills_item = skills_item_data.to_dict()
                skills.append(skills_item)



        tools: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.tools, Unset):
            tools = []
            for tools_item_data in self.tools:
                tools_item = tools_item_data.to_dict()
                tools.append(tools_item)



        toolsets: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.toolsets, Unset):
            toolsets = []
            for toolsets_item_data in self.toolsets:
                toolsets_item = toolsets_item_data.to_dict()
                toolsets.append(toolsets_item)



        web_search_enabled = self.web_search_enabled


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "model": model,
            "model_config": model_config,
            "name": name,
            "system": system,
        })
        if built_in_integrations is not UNSET:
            field_dict["built_in_integrations"] = built_in_integrations
        if default_credential_refs is not UNSET:
            field_dict["default_credential_refs"] = default_credential_refs
        if default_project_id is not UNSET:
            field_dict["default_project_id"] = default_project_id
        if default_rubric is not UNSET:
            field_dict["default_rubric"] = default_rubric
        if default_vault_ids is not UNSET:
            field_dict["default_vault_ids"] = default_vault_ids
        if description is not UNSET:
            field_dict["description"] = description
        if disabled_integration_mcp_providers is not UNSET:
            field_dict["disabled_integration_mcp_providers"] = disabled_integration_mcp_providers
        if max_concurrent_sessions is not UNSET:
            field_dict["max_concurrent_sessions"] = max_concurrent_sessions
        if mcp_servers is not UNSET:
            field_dict["mcp_servers"] = mcp_servers
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if multiagent is not UNSET:
            field_dict["multiagent"] = multiagent
        if native_integrations is not UNSET:
            field_dict["nativeIntegrations"] = native_integrations
        if skills is not UNSET:
            field_dict["skills"] = skills
        if tools is not UNSET:
            field_dict["tools"] = tools
        if toolsets is not UNSET:
            field_dict["toolsets"] = toolsets
        if web_search_enabled is not UNSET:
            field_dict["web_search_enabled"] = web_search_enabled

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_agent_template_definition_mcp_servers_item import ManagedAgentsAgentTemplateDefinitionMcpServersItem # noqa: PLC0415
        from ..models.managed_agents_agent_template_definition_metadata import ManagedAgentsAgentTemplateDefinitionMetadata # noqa: PLC0415
        from ..models.managed_agents_agent_template_definition_multiagent import ManagedAgentsAgentTemplateDefinitionMultiagent # noqa: PLC0415
        from ..models.managed_agents_agent_template_definition_skills_item import ManagedAgentsAgentTemplateDefinitionSkillsItem # noqa: PLC0415
        from ..models.managed_agents_agent_template_definition_tools_item import ManagedAgentsAgentTemplateDefinitionToolsItem # noqa: PLC0415
        from ..models.managed_agents_agent_template_definition_toolsets_item import ManagedAgentsAgentTemplateDefinitionToolsetsItem # noqa: PLC0415
        from ..models.managed_agents_built_in_integration import ManagedAgentsBuiltInIntegration # noqa: PLC0415
        from ..models.managed_agents_inference_config import ManagedAgentsInferenceConfig # noqa: PLC0415
        from ..models.managed_agents_native_integration import ManagedAgentsNativeIntegration # noqa: PLC0415
        from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef # noqa: PLC0415
        d = dict(src_dict)
        model = d.pop("model")

        model_config = ManagedAgentsInferenceConfig.from_dict(d.pop("model_config"))




        name = d.pop("name")

        system = d.pop("system")

        _built_in_integrations = d.pop("built_in_integrations", UNSET)
        built_in_integrations: list[ManagedAgentsBuiltInIntegration] | Unset = UNSET
        if _built_in_integrations is not UNSET:
            built_in_integrations = []
            for built_in_integrations_item_data in _built_in_integrations:
                built_in_integrations_item = ManagedAgentsBuiltInIntegration.from_dict(built_in_integrations_item_data)



                built_in_integrations.append(built_in_integrations_item)


        _default_credential_refs = d.pop("default_credential_refs", UNSET)
        default_credential_refs: list[ManagedAgentsVaultCredentialRef] | Unset = UNSET
        if _default_credential_refs is not UNSET:
            default_credential_refs = []
            for default_credential_refs_item_data in _default_credential_refs:
                default_credential_refs_item = ManagedAgentsVaultCredentialRef.from_dict(default_credential_refs_item_data)



                default_credential_refs.append(default_credential_refs_item)


        default_project_id = d.pop("default_project_id", UNSET)

        default_rubric = d.pop("default_rubric", UNSET)

        default_vault_ids = cast(list[str], d.pop("default_vault_ids", UNSET))


        description = d.pop("description", UNSET)

        disabled_integration_mcp_providers = cast(list[str], d.pop("disabled_integration_mcp_providers", UNSET))


        max_concurrent_sessions = d.pop("max_concurrent_sessions", UNSET)

        _mcp_servers = d.pop("mcp_servers", UNSET)
        mcp_servers: list[ManagedAgentsAgentTemplateDefinitionMcpServersItem] | Unset = UNSET
        if _mcp_servers is not UNSET:
            mcp_servers = []
            for mcp_servers_item_data in _mcp_servers:
                mcp_servers_item = ManagedAgentsAgentTemplateDefinitionMcpServersItem.from_dict(mcp_servers_item_data)



                mcp_servers.append(mcp_servers_item)


        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsAgentTemplateDefinitionMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsAgentTemplateDefinitionMetadata.from_dict(_metadata)




        _multiagent = d.pop("multiagent", UNSET)
        multiagent: ManagedAgentsAgentTemplateDefinitionMultiagent | Unset
        if isinstance(_multiagent,  Unset):
            multiagent = UNSET
        else:
            multiagent = ManagedAgentsAgentTemplateDefinitionMultiagent.from_dict(_multiagent)




        _native_integrations = d.pop("nativeIntegrations", UNSET)
        native_integrations: list[ManagedAgentsNativeIntegration] | Unset = UNSET
        if _native_integrations is not UNSET:
            native_integrations = []
            for native_integrations_item_data in _native_integrations:
                native_integrations_item = ManagedAgentsNativeIntegration.from_dict(native_integrations_item_data)



                native_integrations.append(native_integrations_item)


        _skills = d.pop("skills", UNSET)
        skills: list[ManagedAgentsAgentTemplateDefinitionSkillsItem] | Unset = UNSET
        if _skills is not UNSET:
            skills = []
            for skills_item_data in _skills:
                skills_item = ManagedAgentsAgentTemplateDefinitionSkillsItem.from_dict(skills_item_data)



                skills.append(skills_item)


        _tools = d.pop("tools", UNSET)
        tools: list[ManagedAgentsAgentTemplateDefinitionToolsItem] | Unset = UNSET
        if _tools is not UNSET:
            tools = []
            for tools_item_data in _tools:
                tools_item = ManagedAgentsAgentTemplateDefinitionToolsItem.from_dict(tools_item_data)



                tools.append(tools_item)


        _toolsets = d.pop("toolsets", UNSET)
        toolsets: list[ManagedAgentsAgentTemplateDefinitionToolsetsItem] | Unset = UNSET
        if _toolsets is not UNSET:
            toolsets = []
            for toolsets_item_data in _toolsets:
                toolsets_item = ManagedAgentsAgentTemplateDefinitionToolsetsItem.from_dict(toolsets_item_data)



                toolsets.append(toolsets_item)


        web_search_enabled = d.pop("web_search_enabled", UNSET)

        managed_agents_agent_template_definition = cls(
            model=model,
            model_config=model_config,
            name=name,
            system=system,
            built_in_integrations=built_in_integrations,
            default_credential_refs=default_credential_refs,
            default_project_id=default_project_id,
            default_rubric=default_rubric,
            default_vault_ids=default_vault_ids,
            description=description,
            disabled_integration_mcp_providers=disabled_integration_mcp_providers,
            max_concurrent_sessions=max_concurrent_sessions,
            mcp_servers=mcp_servers,
            metadata=metadata,
            multiagent=multiagent,
            native_integrations=native_integrations,
            skills=skills,
            tools=tools,
            toolsets=toolsets,
            web_search_enabled=web_search_enabled,
        )


        managed_agents_agent_template_definition.additional_properties = d
        return managed_agents_agent_template_definition

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
