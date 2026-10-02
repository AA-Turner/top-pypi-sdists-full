from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_agent_mcp_servers_type_0_item import ManagedAgentsAgentMcpServersType0Item
  from ..models.managed_agents_agent_metadata import ManagedAgentsAgentMetadata
  from ..models.managed_agents_agent_multiagent import ManagedAgentsAgentMultiagent
  from ..models.managed_agents_agent_skills_type_0_item import ManagedAgentsAgentSkillsType0Item
  from ..models.managed_agents_agent_toolsets_type_0_item import ManagedAgentsAgentToolsetsType0Item
  from ..models.managed_agents_built_in_integration import ManagedAgentsBuiltInIntegration
  from ..models.managed_agents_inference_config import ManagedAgentsInferenceConfig
  from ..models.managed_agents_native_integration import ManagedAgentsNativeIntegration
  from ..models.managed_agents_tag import ManagedAgentsTag
  from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef





T = TypeVar("T", bound="ManagedAgentsAgent")



@_attrs_define
class ManagedAgentsAgent:
    """ A configured agent: its versioned execution definition plus current mutable classification tags. Publishing the
    execution definition mints a new immutable AgentVersion; applying tags does not. A session records the version it
    ran and never snapshots tags.

        Example:
            {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'built_in_integrations': [{'connection_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'tools': ['example']}], 'created_at': '2026-02-18T09:30:00Z',
                'default_credential_refs': [{'credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'default_project_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'default_rubric': 'example', 'default_vault_ids': ['example'], 'description': 'example',
                'disabled_integration_mcp_providers': ['example'], 'latest_agent_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'max_concurrent_sessions': 1, 'mcp_servers': [{'key': 'example'}],
                'metadata': {'key': 'example'}, 'model': 'example', 'model_config': {'max_tokens': 1, 'provider_params': {'key':
                'example'}, 'reasoning_effort': 'example', 'temperature': 1.5, 'top_p': 1.5}, 'multiagent': {'key': 'example'},
                'name': 'example-name', 'nativeIntegrations': [{'connectionId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'permission': 'example', 'resources': ['example']}], 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'skills': [{'key': 'example'}], 'system': 'example', 'tags': [{'color': '#14b8a6', 'created_at':
                '2026-02-18T09:30:00Z', 'description': 'example', 'label': 'example', 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'tag_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at':
                '2026-02-18T09:30:00Z'}], 'toolsets': [{'type': 'evaluation'}], 'updated_at': '2026-02-18T09:30:00Z',
                'web_search_enabled': True}

        Attributes:
            agent_id (str): Server-assigned id of the agent, used in the agent, agent-version, and session routes.
            created_at (datetime.datetime): Server-assigned RFC 3339 timestamp of when the agent was created.
            default_credential_refs (list[ManagedAgentsVaultCredentialRef] | None): Narrows the default vaults to individual
                credentials. Every credential is selected when a vault is first added, and may then be unchecked.
            default_vault_ids (list[str] | None): Vaults whose credentials are copied into a new session when its create
                request omits vault_ids. Sending an explicit empty list on the session still overrides these.
            disabled_integration_mcp_providers (list[str] | None): Native integration providers whose MCP tools new sessions
                of this agent do not receive, even though the grant is present. The grant still authenticates the provider's
                sandbox tools where it has any (git and gh for GitHub). Suppresses integration-derived servers only, never the
                agent's own mcp_servers. New agents decline github by default when the field is omitted on create (JSON null
                counts as omitted); send an explicit [] on create to receive every provider's MCP tools. A version write carries
                the list in full: omitting it publishes a version with none.
            mcp_servers (list[ManagedAgentsAgentMcpServersType0Item] | None): Remote MCP servers to attach. Each entry is an
                object with name (the label the server's tools are grouped under) and url (its http/https endpoint); any further
                keys are passed to the runtime unchanged. Credentials come from the vaults granted to the session, not from this
                entry. Tools are discovered and snapshotted at session start.
            model (str): Model the agent runs on. Pass a gateway model id exactly as the gateway models catalog reports it,
                e.g. anthropic/claude-sonnet-4-5; it is stored prefixed as litellm:anthropic/claude-sonnet-4-5, which is the
                form the router reads and the form returned on reads. An explicitly provider-qualified string such as
                anthropic:claude-sonnet-4-5 selects a directly-configured provider instead and is left as written. An id the
                gateway does not serve is rejected here, not at the session's first turn.
            model_config (ManagedAgentsInferenceConfig): Sampling and generation settings for a model call, mirroring the
                provider's own request parameters. Set it on an agent or a session to govern every turn, and read it back on a
                model event to see what the call actually used. Example: {'max_tokens': 1, 'provider_params': {'key':
                'example'}, 'reasoning_effort': 'example', 'temperature': 1.5, 'top_p': 1.5}.
            name (str): Human-readable label shown wherever agents are listed. Not required to be unique.
            organization_id (str): Organization that owns the agent. Server-assigned from the caller's credentials; a value
                sent in a request body is ignored.
            skills (list[ManagedAgentsAgentSkillsType0Item] | None): Skill packages loaded into the agent's runtime, each an
                entry with the skill reference and its metadata.
            system (str): System prompt prepended to every conversation this agent runs.
            tags (list[ManagedAgentsTag]): Current organization-scoped classification tags applied to this agent. Always an
                array. Tags are mutable catalog metadata and are deliberately absent from AgentVersion and session runtime
                snapshots.
            toolsets (list[ManagedAgentsAgentToolsetsType0Item] | None): The bare evaluation marker, when this is an
                evaluator agent. Historical stored agents may contain ignored declarations, omitted from current API responses.
                Built-in sandbox tools need no marker.
            updated_at (datetime.datetime): Server-assigned RFC 3339 timestamp of the most recent update to the agent.
            built_in_integrations (list[ManagedAgentsBuiltInIntegration] | Unset): Vendor integrations this agent may use,
                each naming an active organization connection an admin configured on the Integrations page (provider merge).
                Sessions receive a short-lived credential restricted to exactly those vendors and the admin's tool allow-list
                for each, delivered to the sandbox for the merge CLI. Not a vault grant: nothing about these appears under
                credential access. A version write carries the list in full: omitting it publishes a version with none.
            default_project_id (str | Unset): Labelbox project copied into new sessions when their create request omits
                project_id. A non-empty session project_id overrides it. Carried in full on every version write: omitting it
                publishes a version with no default.
            default_rubric (str | Unset): Markdown rubric that sessions started from this agent are graded against when
                their create request omits an outcome. A session that supplies its own outcome ignores this entirely. Carried in
                full on every version write: omitting it publishes a version with no rubric.
            description (str | Unset): Free-text note about what this agent is for.
            latest_agent_version_id (str | Unset): Server-maintained id of the newest version of this agent; sessions
                started without an explicit version use it.
            max_concurrent_sessions (int | Unset): Maximum number of this agent's root sessions that may run or wait on
                compute at once. Omit for unlimited. Sessions beyond the cap are accepted with execution_state=queued and wait
                until a slot frees; child/subagent sessions do not count. Carried in full on every version write: omitting it
                publishes a version with no cap.
            metadata (ManagedAgentsAgentMetadata | Unset): Caller-owned key/value data stored with the agent and returned
                unchanged.
            multiagent (ManagedAgentsAgentMultiagent | Unset): Multi-agent orchestration settings, such as subagent
                definitions and delegation limits.
            native_integrations (list[ManagedAgentsNativeIntegration] | Unset): Native connections this agent may use, with
                provider-enforced permission and resource restrictions. Omit or send [] for none. Stored in full on each agent
                version; secrets remain on the connection.
            web_search_enabled (bool | Unset): Whether new sessions may use the native web_search tool. Omitted on legacy
                agents and interpreted as enabled. Default: True.
     """

    agent_id: str
    created_at: datetime.datetime
    default_credential_refs: list[ManagedAgentsVaultCredentialRef] | None
    default_vault_ids: list[str] | None
    disabled_integration_mcp_providers: list[str] | None
    mcp_servers: list[ManagedAgentsAgentMcpServersType0Item] | None
    model: str
    model_config: ManagedAgentsInferenceConfig
    name: str
    organization_id: str
    skills: list[ManagedAgentsAgentSkillsType0Item] | None
    system: str
    tags: list[ManagedAgentsTag]
    toolsets: list[ManagedAgentsAgentToolsetsType0Item] | None
    updated_at: datetime.datetime
    built_in_integrations: list[ManagedAgentsBuiltInIntegration] | Unset = UNSET
    default_project_id: str | Unset = UNSET
    default_rubric: str | Unset = UNSET
    description: str | Unset = UNSET
    latest_agent_version_id: str | Unset = UNSET
    max_concurrent_sessions: int | Unset = UNSET
    metadata: ManagedAgentsAgentMetadata | Unset = UNSET
    multiagent: ManagedAgentsAgentMultiagent | Unset = UNSET
    native_integrations: list[ManagedAgentsNativeIntegration] | Unset = UNSET
    web_search_enabled: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_agent_mcp_servers_type_0_item import ManagedAgentsAgentMcpServersType0Item # noqa: PLC0415
        from ..models.managed_agents_agent_metadata import ManagedAgentsAgentMetadata # noqa: PLC0415
        from ..models.managed_agents_agent_multiagent import ManagedAgentsAgentMultiagent # noqa: PLC0415
        from ..models.managed_agents_agent_skills_type_0_item import ManagedAgentsAgentSkillsType0Item # noqa: PLC0415
        from ..models.managed_agents_agent_toolsets_type_0_item import ManagedAgentsAgentToolsetsType0Item # noqa: PLC0415
        from ..models.managed_agents_built_in_integration import ManagedAgentsBuiltInIntegration # noqa: PLC0415
        from ..models.managed_agents_inference_config import ManagedAgentsInferenceConfig # noqa: PLC0415
        from ..models.managed_agents_native_integration import ManagedAgentsNativeIntegration # noqa: PLC0415
        from ..models.managed_agents_tag import ManagedAgentsTag # noqa: PLC0415
        from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef # noqa: PLC0415
        agent_id = self.agent_id

        created_at = self.created_at.isoformat()

        default_credential_refs: list[dict[str, Any]] | None
        if isinstance(self.default_credential_refs, list):
            default_credential_refs = []
            for default_credential_refs_type_0_item_data in self.default_credential_refs:
                default_credential_refs_type_0_item = default_credential_refs_type_0_item_data.to_dict()
                default_credential_refs.append(default_credential_refs_type_0_item)


        else:
            default_credential_refs = self.default_credential_refs

        default_vault_ids: list[str] | None
        if isinstance(self.default_vault_ids, list):
            default_vault_ids = self.default_vault_ids


        else:
            default_vault_ids = self.default_vault_ids

        disabled_integration_mcp_providers: list[str] | None
        if isinstance(self.disabled_integration_mcp_providers, list):
            disabled_integration_mcp_providers = self.disabled_integration_mcp_providers


        else:
            disabled_integration_mcp_providers = self.disabled_integration_mcp_providers

        mcp_servers: list[dict[str, Any]] | None
        if isinstance(self.mcp_servers, list):
            mcp_servers = []
            for mcp_servers_type_0_item_data in self.mcp_servers:
                mcp_servers_type_0_item = mcp_servers_type_0_item_data.to_dict()
                mcp_servers.append(mcp_servers_type_0_item)


        else:
            mcp_servers = self.mcp_servers

        model = self.model

        model_config = self.model_config.to_dict()

        name = self.name

        organization_id = self.organization_id

        skills: list[dict[str, Any]] | None
        if isinstance(self.skills, list):
            skills = []
            for skills_type_0_item_data in self.skills:
                skills_type_0_item = skills_type_0_item_data.to_dict()
                skills.append(skills_type_0_item)


        else:
            skills = self.skills

        system = self.system

        tags = []
        for tags_item_data in self.tags:
            tags_item = tags_item_data.to_dict()
            tags.append(tags_item)



        toolsets: list[dict[str, Any]] | None
        if isinstance(self.toolsets, list):
            toolsets = []
            for toolsets_type_0_item_data in self.toolsets:
                toolsets_type_0_item = toolsets_type_0_item_data.to_dict()
                toolsets.append(toolsets_type_0_item)


        else:
            toolsets = self.toolsets

        updated_at = self.updated_at.isoformat()

        built_in_integrations: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.built_in_integrations, Unset):
            built_in_integrations = []
            for built_in_integrations_item_data in self.built_in_integrations:
                built_in_integrations_item = built_in_integrations_item_data.to_dict()
                built_in_integrations.append(built_in_integrations_item)



        default_project_id = self.default_project_id

        default_rubric = self.default_rubric

        description = self.description

        latest_agent_version_id = self.latest_agent_version_id

        max_concurrent_sessions = self.max_concurrent_sessions

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



        web_search_enabled = self.web_search_enabled


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "agent_id": agent_id,
            "created_at": created_at,
            "default_credential_refs": default_credential_refs,
            "default_vault_ids": default_vault_ids,
            "disabled_integration_mcp_providers": disabled_integration_mcp_providers,
            "mcp_servers": mcp_servers,
            "model": model,
            "model_config": model_config,
            "name": name,
            "organization_id": organization_id,
            "skills": skills,
            "system": system,
            "tags": tags,
            "toolsets": toolsets,
            "updated_at": updated_at,
        })
        if built_in_integrations is not UNSET:
            field_dict["built_in_integrations"] = built_in_integrations
        if default_project_id is not UNSET:
            field_dict["default_project_id"] = default_project_id
        if default_rubric is not UNSET:
            field_dict["default_rubric"] = default_rubric
        if description is not UNSET:
            field_dict["description"] = description
        if latest_agent_version_id is not UNSET:
            field_dict["latest_agent_version_id"] = latest_agent_version_id
        if max_concurrent_sessions is not UNSET:
            field_dict["max_concurrent_sessions"] = max_concurrent_sessions
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if multiagent is not UNSET:
            field_dict["multiagent"] = multiagent
        if native_integrations is not UNSET:
            field_dict["nativeIntegrations"] = native_integrations
        if web_search_enabled is not UNSET:
            field_dict["web_search_enabled"] = web_search_enabled

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_agent_mcp_servers_type_0_item import ManagedAgentsAgentMcpServersType0Item # noqa: PLC0415
        from ..models.managed_agents_agent_metadata import ManagedAgentsAgentMetadata # noqa: PLC0415
        from ..models.managed_agents_agent_multiagent import ManagedAgentsAgentMultiagent # noqa: PLC0415
        from ..models.managed_agents_agent_skills_type_0_item import ManagedAgentsAgentSkillsType0Item # noqa: PLC0415
        from ..models.managed_agents_agent_toolsets_type_0_item import ManagedAgentsAgentToolsetsType0Item # noqa: PLC0415
        from ..models.managed_agents_built_in_integration import ManagedAgentsBuiltInIntegration # noqa: PLC0415
        from ..models.managed_agents_inference_config import ManagedAgentsInferenceConfig # noqa: PLC0415
        from ..models.managed_agents_native_integration import ManagedAgentsNativeIntegration # noqa: PLC0415
        from ..models.managed_agents_tag import ManagedAgentsTag # noqa: PLC0415
        from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef # noqa: PLC0415
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        def _parse_default_credential_refs(data: object) -> list[ManagedAgentsVaultCredentialRef] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                default_credential_refs_type_0 = []
                _default_credential_refs_type_0 = data
                for default_credential_refs_type_0_item_data in (_default_credential_refs_type_0):
                    default_credential_refs_type_0_item = ManagedAgentsVaultCredentialRef.from_dict(default_credential_refs_type_0_item_data)



                    default_credential_refs_type_0.append(default_credential_refs_type_0_item)

                return default_credential_refs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsVaultCredentialRef] | None, data)

        default_credential_refs = _parse_default_credential_refs(d.pop("default_credential_refs"))


        def _parse_default_vault_ids(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                default_vault_ids_type_0 = cast(list[str], data)

                return default_vault_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        default_vault_ids = _parse_default_vault_ids(d.pop("default_vault_ids"))


        def _parse_disabled_integration_mcp_providers(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                disabled_integration_mcp_providers_type_0 = cast(list[str], data)

                return disabled_integration_mcp_providers_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        disabled_integration_mcp_providers = _parse_disabled_integration_mcp_providers(d.pop("disabled_integration_mcp_providers"))


        def _parse_mcp_servers(data: object) -> list[ManagedAgentsAgentMcpServersType0Item] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                mcp_servers_type_0 = []
                _mcp_servers_type_0 = data
                for mcp_servers_type_0_item_data in (_mcp_servers_type_0):
                    mcp_servers_type_0_item = ManagedAgentsAgentMcpServersType0Item.from_dict(mcp_servers_type_0_item_data)



                    mcp_servers_type_0.append(mcp_servers_type_0_item)

                return mcp_servers_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsAgentMcpServersType0Item] | None, data)

        mcp_servers = _parse_mcp_servers(d.pop("mcp_servers"))


        model = d.pop("model")

        model_config = ManagedAgentsInferenceConfig.from_dict(d.pop("model_config"))




        name = d.pop("name")

        organization_id = d.pop("organization_id")

        def _parse_skills(data: object) -> list[ManagedAgentsAgentSkillsType0Item] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                skills_type_0 = []
                _skills_type_0 = data
                for skills_type_0_item_data in (_skills_type_0):
                    skills_type_0_item = ManagedAgentsAgentSkillsType0Item.from_dict(skills_type_0_item_data)



                    skills_type_0.append(skills_type_0_item)

                return skills_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsAgentSkillsType0Item] | None, data)

        skills = _parse_skills(d.pop("skills"))


        system = d.pop("system")

        tags = []
        _tags = d.pop("tags")
        for tags_item_data in (_tags):
            tags_item = ManagedAgentsTag.from_dict(tags_item_data)



            tags.append(tags_item)


        def _parse_toolsets(data: object) -> list[ManagedAgentsAgentToolsetsType0Item] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                toolsets_type_0 = []
                _toolsets_type_0 = data
                for toolsets_type_0_item_data in (_toolsets_type_0):
                    toolsets_type_0_item = ManagedAgentsAgentToolsetsType0Item.from_dict(toolsets_type_0_item_data)



                    toolsets_type_0.append(toolsets_type_0_item)

                return toolsets_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsAgentToolsetsType0Item] | None, data)

        toolsets = _parse_toolsets(d.pop("toolsets"))


        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        _built_in_integrations = d.pop("built_in_integrations", UNSET)
        built_in_integrations: list[ManagedAgentsBuiltInIntegration] | Unset = UNSET
        if _built_in_integrations is not UNSET:
            built_in_integrations = []
            for built_in_integrations_item_data in _built_in_integrations:
                built_in_integrations_item = ManagedAgentsBuiltInIntegration.from_dict(built_in_integrations_item_data)



                built_in_integrations.append(built_in_integrations_item)


        default_project_id = d.pop("default_project_id", UNSET)

        default_rubric = d.pop("default_rubric", UNSET)

        description = d.pop("description", UNSET)

        latest_agent_version_id = d.pop("latest_agent_version_id", UNSET)

        max_concurrent_sessions = d.pop("max_concurrent_sessions", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsAgentMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsAgentMetadata.from_dict(_metadata)




        _multiagent = d.pop("multiagent", UNSET)
        multiagent: ManagedAgentsAgentMultiagent | Unset
        if isinstance(_multiagent,  Unset):
            multiagent = UNSET
        else:
            multiagent = ManagedAgentsAgentMultiagent.from_dict(_multiagent)




        _native_integrations = d.pop("nativeIntegrations", UNSET)
        native_integrations: list[ManagedAgentsNativeIntegration] | Unset = UNSET
        if _native_integrations is not UNSET:
            native_integrations = []
            for native_integrations_item_data in _native_integrations:
                native_integrations_item = ManagedAgentsNativeIntegration.from_dict(native_integrations_item_data)



                native_integrations.append(native_integrations_item)


        web_search_enabled = d.pop("web_search_enabled", UNSET)

        managed_agents_agent = cls(
            agent_id=agent_id,
            created_at=created_at,
            default_credential_refs=default_credential_refs,
            default_vault_ids=default_vault_ids,
            disabled_integration_mcp_providers=disabled_integration_mcp_providers,
            mcp_servers=mcp_servers,
            model=model,
            model_config=model_config,
            name=name,
            organization_id=organization_id,
            skills=skills,
            system=system,
            tags=tags,
            toolsets=toolsets,
            updated_at=updated_at,
            built_in_integrations=built_in_integrations,
            default_project_id=default_project_id,
            default_rubric=default_rubric,
            description=description,
            latest_agent_version_id=latest_agent_version_id,
            max_concurrent_sessions=max_concurrent_sessions,
            metadata=metadata,
            multiagent=multiagent,
            native_integrations=native_integrations,
            web_search_enabled=web_search_enabled,
        )


        managed_agents_agent.additional_properties = d
        return managed_agents_agent

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
