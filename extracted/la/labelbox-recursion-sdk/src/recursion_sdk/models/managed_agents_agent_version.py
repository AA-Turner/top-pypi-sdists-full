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
  from ..models.managed_agents_agent_version_mcp_servers_type_0_item import ManagedAgentsAgentVersionMcpServersType0Item
  from ..models.managed_agents_agent_version_metadata import ManagedAgentsAgentVersionMetadata
  from ..models.managed_agents_agent_version_multiagent import ManagedAgentsAgentVersionMultiagent
  from ..models.managed_agents_agent_version_skills_type_0_item import ManagedAgentsAgentVersionSkillsType0Item
  from ..models.managed_agents_agent_version_toolsets_type_0_item import ManagedAgentsAgentVersionToolsetsType0Item
  from ..models.managed_agents_built_in_integration import ManagedAgentsBuiltInIntegration
  from ..models.managed_agents_inference_config import ManagedAgentsInferenceConfig
  from ..models.managed_agents_native_integration import ManagedAgentsNativeIntegration
  from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef





T = TypeVar("T", bound="ManagedAgentsAgentVersion")



@_attrs_define
class ManagedAgentsAgentVersion:
    """ An immutable snapshot of an agent's configuration, minted on every update. Sessions reference a version rather than
    the agent, so a running session's behaviour cannot change under it.

        Example:
            {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'built_in_integrations': [{'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'tools': ['example']}],
                'created_at': '2026-02-18T09:30:00Z', 'created_by': 'example', 'default_credential_refs': [{'credential_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}],
                'default_project_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'default_rubric': 'example', 'default_vault_ids':
                ['example'], 'description': 'example', 'disabled_integration_mcp_providers': ['example'],
                'max_concurrent_sessions': 1, 'mcp_servers': [{'key': 'example'}], 'metadata': {'key': 'example'}, 'model':
                'example', 'model_config': {'max_tokens': 1, 'provider_params': {'key': 'example'}, 'reasoning_effort':
                'example', 'temperature': 1.5, 'top_p': 1.5}, 'multiagent': {'key': 'example'}, 'name': 'example-name',
                'nativeIntegrations': [{'connectionId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'permission': 'example',
                'resources': ['example']}], 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'skills': [{'key':
                'example'}], 'system': 'example', 'toolsets': [{'type': 'evaluation'}], 'version_number': 1,
                'web_search_enabled': True}

        Attributes:
            agent_id (str): Agent this version belongs to (UUID).
            agent_version_id (str): Identifier for this agent version (UUID). Server-assigned. Pass it when starting a
                session that must run a specific version.
            created_at (datetime.datetime): RFC 3339 timestamp of when this record was created. Server-assigned.
            default_credential_refs (list[ManagedAgentsVaultCredentialRef] | None): Narrows this version's default vaults to
                individual credentials.
            default_vault_ids (list[str] | None): Vaults whose credentials are copied into a new session started from this
                version when the create request omits vault_ids.
            disabled_integration_mcp_providers (list[str] | None): Native integration providers whose MCP tools sessions
                started from this version do not receive. The grant and its sandbox credentials are unaffected.
            mcp_servers (list[ManagedAgentsAgentVersionMcpServersType0Item] | None): Remote MCP servers attached at this
                version. Each entry is an object with name and url (http/https); further keys pass to the runtime unchanged.
                Credentials come from the session's granted vaults.
            model_config (ManagedAgentsInferenceConfig): Sampling and generation settings for a model call, mirroring the
                provider's own request parameters. Set it on an agent or a session to govern every turn, and read it back on a
                model event to see what the call actually used. Example: {'max_tokens': 1, 'provider_params': {'key':
                'example'}, 'reasoning_effort': 'example', 'temperature': 1.5, 'top_p': 1.5}.
            name (str): The agent's human-readable label as it stood at this version.
            organization_id (str): Organization that owns this record. Resolved from the API key; never accepted from the
                caller.
            skills (list[ManagedAgentsAgentVersionSkillsType0Item] | None): Skill packages loaded into the runtime at this
                version, each an entry with the skill reference and its metadata.
            system (str): System prompt this version prepends to every conversation.
            toolsets (list[ManagedAgentsAgentVersionToolsetsType0Item] | None): The bare evaluation marker, when this is an
                evaluator version. Historical stored versions may contain ignored declarations, omitted from current API
                responses. Built-in sandbox tools need no marker.
            version_number (int): Monotonically increasing version counter within the agent, starting at 1. Server-assigned.
            built_in_integrations (list[ManagedAgentsBuiltInIntegration] | Unset): Vendor integrations sessions started from
                this version may use, each naming an admin-configured organization connection. Snapshotted with the version.
            created_by (str | Unset): User who made the edit that produced this version, for audit. Empty when the version
                was created by an automated caller.
            default_project_id (str | Unset): Labelbox project copied into sessions started from this version when their
                create request omits project_id. A non-empty session project_id overrides it.
            default_rubric (str | Unset): Markdown rubric that sessions started from this version are graded against when
                their create request omits an outcome. A session that supplies its own outcome ignores this entirely.
            description (str | Unset): The agent's free-text note as it stood at this version.
            max_concurrent_sessions (int | Unset): Maximum concurrent root sessions configured on the agent when this
                version was minted. Unset means unlimited. Live admission uses the agent head's current value, not this
                snapshot.
            metadata (ManagedAgentsAgentVersionMetadata | Unset): Free-form caller-supplied key/value labels. Stored
                verbatim and never interpreted by the service.
            model (str | Unset): Model this version runs on, in the same form as an agent's model: a gateway catalog id such
                as anthropic/claude-sonnet-4-5, stored and returned prefixed as litellm:anthropic/claude-sonnet-4-5.
            multiagent (ManagedAgentsAgentVersionMultiagent | Unset): Multi-agent orchestration settings at this version,
                such as subagent definitions and delegation limits.
            native_integrations (list[ManagedAgentsNativeIntegration] | Unset): Native connections this agent may use, with
                provider-enforced permission and resource restrictions. Omit or send [] for none. Stored in full on each agent
                version; secrets remain on the connection.
            web_search_enabled (bool | Unset): Whether sessions created from this version may use the native web_search
                tool. Omitted on legacy versions and interpreted as enabled. Default: True.
     """

    agent_id: str
    agent_version_id: str
    created_at: datetime.datetime
    default_credential_refs: list[ManagedAgentsVaultCredentialRef] | None
    default_vault_ids: list[str] | None
    disabled_integration_mcp_providers: list[str] | None
    mcp_servers: list[ManagedAgentsAgentVersionMcpServersType0Item] | None
    model_config: ManagedAgentsInferenceConfig
    name: str
    organization_id: str
    skills: list[ManagedAgentsAgentVersionSkillsType0Item] | None
    system: str
    toolsets: list[ManagedAgentsAgentVersionToolsetsType0Item] | None
    version_number: int
    built_in_integrations: list[ManagedAgentsBuiltInIntegration] | Unset = UNSET
    created_by: str | Unset = UNSET
    default_project_id: str | Unset = UNSET
    default_rubric: str | Unset = UNSET
    description: str | Unset = UNSET
    max_concurrent_sessions: int | Unset = UNSET
    metadata: ManagedAgentsAgentVersionMetadata | Unset = UNSET
    model: str | Unset = UNSET
    multiagent: ManagedAgentsAgentVersionMultiagent | Unset = UNSET
    native_integrations: list[ManagedAgentsNativeIntegration] | Unset = UNSET
    web_search_enabled: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_agent_version_mcp_servers_type_0_item import ManagedAgentsAgentVersionMcpServersType0Item # noqa: PLC0415
        from ..models.managed_agents_agent_version_metadata import ManagedAgentsAgentVersionMetadata # noqa: PLC0415
        from ..models.managed_agents_agent_version_multiagent import ManagedAgentsAgentVersionMultiagent # noqa: PLC0415
        from ..models.managed_agents_agent_version_skills_type_0_item import ManagedAgentsAgentVersionSkillsType0Item # noqa: PLC0415
        from ..models.managed_agents_agent_version_toolsets_type_0_item import ManagedAgentsAgentVersionToolsetsType0Item # noqa: PLC0415
        from ..models.managed_agents_built_in_integration import ManagedAgentsBuiltInIntegration # noqa: PLC0415
        from ..models.managed_agents_inference_config import ManagedAgentsInferenceConfig # noqa: PLC0415
        from ..models.managed_agents_native_integration import ManagedAgentsNativeIntegration # noqa: PLC0415
        from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef # noqa: PLC0415
        agent_id = self.agent_id

        agent_version_id = self.agent_version_id

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

        toolsets: list[dict[str, Any]] | None
        if isinstance(self.toolsets, list):
            toolsets = []
            for toolsets_type_0_item_data in self.toolsets:
                toolsets_type_0_item = toolsets_type_0_item_data.to_dict()
                toolsets.append(toolsets_type_0_item)


        else:
            toolsets = self.toolsets

        version_number = self.version_number

        built_in_integrations: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.built_in_integrations, Unset):
            built_in_integrations = []
            for built_in_integrations_item_data in self.built_in_integrations:
                built_in_integrations_item = built_in_integrations_item_data.to_dict()
                built_in_integrations.append(built_in_integrations_item)



        created_by = self.created_by

        default_project_id = self.default_project_id

        default_rubric = self.default_rubric

        description = self.description

        max_concurrent_sessions = self.max_concurrent_sessions

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        model = self.model

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
            "agent_version_id": agent_version_id,
            "created_at": created_at,
            "default_credential_refs": default_credential_refs,
            "default_vault_ids": default_vault_ids,
            "disabled_integration_mcp_providers": disabled_integration_mcp_providers,
            "mcp_servers": mcp_servers,
            "model_config": model_config,
            "name": name,
            "organization_id": organization_id,
            "skills": skills,
            "system": system,
            "toolsets": toolsets,
            "version_number": version_number,
        })
        if built_in_integrations is not UNSET:
            field_dict["built_in_integrations"] = built_in_integrations
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if default_project_id is not UNSET:
            field_dict["default_project_id"] = default_project_id
        if default_rubric is not UNSET:
            field_dict["default_rubric"] = default_rubric
        if description is not UNSET:
            field_dict["description"] = description
        if max_concurrent_sessions is not UNSET:
            field_dict["max_concurrent_sessions"] = max_concurrent_sessions
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if model is not UNSET:
            field_dict["model"] = model
        if multiagent is not UNSET:
            field_dict["multiagent"] = multiagent
        if native_integrations is not UNSET:
            field_dict["nativeIntegrations"] = native_integrations
        if web_search_enabled is not UNSET:
            field_dict["web_search_enabled"] = web_search_enabled

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_agent_version_mcp_servers_type_0_item import ManagedAgentsAgentVersionMcpServersType0Item # noqa: PLC0415
        from ..models.managed_agents_agent_version_metadata import ManagedAgentsAgentVersionMetadata # noqa: PLC0415
        from ..models.managed_agents_agent_version_multiagent import ManagedAgentsAgentVersionMultiagent # noqa: PLC0415
        from ..models.managed_agents_agent_version_skills_type_0_item import ManagedAgentsAgentVersionSkillsType0Item # noqa: PLC0415
        from ..models.managed_agents_agent_version_toolsets_type_0_item import ManagedAgentsAgentVersionToolsetsType0Item # noqa: PLC0415
        from ..models.managed_agents_built_in_integration import ManagedAgentsBuiltInIntegration # noqa: PLC0415
        from ..models.managed_agents_inference_config import ManagedAgentsInferenceConfig # noqa: PLC0415
        from ..models.managed_agents_native_integration import ManagedAgentsNativeIntegration # noqa: PLC0415
        from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef # noqa: PLC0415
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        agent_version_id = d.pop("agent_version_id")

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


        def _parse_mcp_servers(data: object) -> list[ManagedAgentsAgentVersionMcpServersType0Item] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                mcp_servers_type_0 = []
                _mcp_servers_type_0 = data
                for mcp_servers_type_0_item_data in (_mcp_servers_type_0):
                    mcp_servers_type_0_item = ManagedAgentsAgentVersionMcpServersType0Item.from_dict(mcp_servers_type_0_item_data)



                    mcp_servers_type_0.append(mcp_servers_type_0_item)

                return mcp_servers_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsAgentVersionMcpServersType0Item] | None, data)

        mcp_servers = _parse_mcp_servers(d.pop("mcp_servers"))


        model_config = ManagedAgentsInferenceConfig.from_dict(d.pop("model_config"))




        name = d.pop("name")

        organization_id = d.pop("organization_id")

        def _parse_skills(data: object) -> list[ManagedAgentsAgentVersionSkillsType0Item] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                skills_type_0 = []
                _skills_type_0 = data
                for skills_type_0_item_data in (_skills_type_0):
                    skills_type_0_item = ManagedAgentsAgentVersionSkillsType0Item.from_dict(skills_type_0_item_data)



                    skills_type_0.append(skills_type_0_item)

                return skills_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsAgentVersionSkillsType0Item] | None, data)

        skills = _parse_skills(d.pop("skills"))


        system = d.pop("system")

        def _parse_toolsets(data: object) -> list[ManagedAgentsAgentVersionToolsetsType0Item] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                toolsets_type_0 = []
                _toolsets_type_0 = data
                for toolsets_type_0_item_data in (_toolsets_type_0):
                    toolsets_type_0_item = ManagedAgentsAgentVersionToolsetsType0Item.from_dict(toolsets_type_0_item_data)



                    toolsets_type_0.append(toolsets_type_0_item)

                return toolsets_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsAgentVersionToolsetsType0Item] | None, data)

        toolsets = _parse_toolsets(d.pop("toolsets"))


        version_number = d.pop("version_number")

        _built_in_integrations = d.pop("built_in_integrations", UNSET)
        built_in_integrations: list[ManagedAgentsBuiltInIntegration] | Unset = UNSET
        if _built_in_integrations is not UNSET:
            built_in_integrations = []
            for built_in_integrations_item_data in _built_in_integrations:
                built_in_integrations_item = ManagedAgentsBuiltInIntegration.from_dict(built_in_integrations_item_data)



                built_in_integrations.append(built_in_integrations_item)


        created_by = d.pop("created_by", UNSET)

        default_project_id = d.pop("default_project_id", UNSET)

        default_rubric = d.pop("default_rubric", UNSET)

        description = d.pop("description", UNSET)

        max_concurrent_sessions = d.pop("max_concurrent_sessions", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsAgentVersionMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsAgentVersionMetadata.from_dict(_metadata)




        model = d.pop("model", UNSET)

        _multiagent = d.pop("multiagent", UNSET)
        multiagent: ManagedAgentsAgentVersionMultiagent | Unset
        if isinstance(_multiagent,  Unset):
            multiagent = UNSET
        else:
            multiagent = ManagedAgentsAgentVersionMultiagent.from_dict(_multiagent)




        _native_integrations = d.pop("nativeIntegrations", UNSET)
        native_integrations: list[ManagedAgentsNativeIntegration] | Unset = UNSET
        if _native_integrations is not UNSET:
            native_integrations = []
            for native_integrations_item_data in _native_integrations:
                native_integrations_item = ManagedAgentsNativeIntegration.from_dict(native_integrations_item_data)



                native_integrations.append(native_integrations_item)


        web_search_enabled = d.pop("web_search_enabled", UNSET)

        managed_agents_agent_version = cls(
            agent_id=agent_id,
            agent_version_id=agent_version_id,
            created_at=created_at,
            default_credential_refs=default_credential_refs,
            default_vault_ids=default_vault_ids,
            disabled_integration_mcp_providers=disabled_integration_mcp_providers,
            mcp_servers=mcp_servers,
            model_config=model_config,
            name=name,
            organization_id=organization_id,
            skills=skills,
            system=system,
            toolsets=toolsets,
            version_number=version_number,
            built_in_integrations=built_in_integrations,
            created_by=created_by,
            default_project_id=default_project_id,
            default_rubric=default_rubric,
            description=description,
            max_concurrent_sessions=max_concurrent_sessions,
            metadata=metadata,
            model=model,
            multiagent=multiagent,
            native_integrations=native_integrations,
            web_search_enabled=web_search_enabled,
        )


        managed_agents_agent_version.additional_properties = d
        return managed_agents_agent_version

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
