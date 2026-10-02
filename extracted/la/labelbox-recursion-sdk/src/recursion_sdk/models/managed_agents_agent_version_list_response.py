from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_agent_version import ManagedAgentsAgentVersion





T = TypeVar("T", bound="ManagedAgentsAgentVersionListResponse")



@_attrs_define
class ManagedAgentsAgentVersionListResponse:
    """ Response body of GET /v1/agents/{agent_id}/versions. Scoped to the one agent in the path, so an empty list means
    that agent has no versions yet, not that no agents exist. Versions are immutable snapshots: pin one to make a
    session reproducible.

        Example:
            {'agent_versions': [{'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'built_in_integrations': [{'connection_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'tools': ['example']}], 'created_at': '2026-02-18T09:30:00Z',
                'created_by': 'example', 'default_credential_refs': [{'credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'default_project_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'default_rubric': 'example', 'default_vault_ids': ['example'],
                'description': 'example', 'disabled_integration_mcp_providers': ['example'], 'max_concurrent_sessions': 1,
                'mcp_servers': [{'key': 'example'}], 'metadata': {'key': 'example'}, 'model': 'example', 'model_config':
                {'max_tokens': 1, 'provider_params': {'key': 'example'}, 'reasoning_effort': 'example', 'temperature': 1.5,
                'top_p': 1.5}, 'multiagent': {'key': 'example'}, 'name': 'example-name', 'nativeIntegrations': [{'connectionId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'permission': 'example', 'resources': ['example']}], 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'skills': [{'key': 'example'}], 'system': 'example', 'toolsets':
                [{'type': 'evaluation'}], 'version_number': 1, 'web_search_enabled': True}]}

        Attributes:
            agent_versions (list[ManagedAgentsAgentVersion] | None): Every published version of the requested agent, newest
                first. Null rather than an empty array when the agent exists but has never been versioned.
     """

    agent_versions: list[ManagedAgentsAgentVersion] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_agent_version import ManagedAgentsAgentVersion # noqa: PLC0415
        agent_versions: list[dict[str, Any]] | None
        if isinstance(self.agent_versions, list):
            agent_versions = []
            for agent_versions_type_0_item_data in self.agent_versions:
                agent_versions_type_0_item = agent_versions_type_0_item_data.to_dict()
                agent_versions.append(agent_versions_type_0_item)


        else:
            agent_versions = self.agent_versions


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "agent_versions": agent_versions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_agent_version import ManagedAgentsAgentVersion # noqa: PLC0415
        d = dict(src_dict)
        def _parse_agent_versions(data: object) -> list[ManagedAgentsAgentVersion] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                agent_versions_type_0 = []
                _agent_versions_type_0 = data
                for agent_versions_type_0_item_data in (_agent_versions_type_0):
                    agent_versions_type_0_item = ManagedAgentsAgentVersion.from_dict(agent_versions_type_0_item_data)



                    agent_versions_type_0.append(agent_versions_type_0_item)

                return agent_versions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsAgentVersion] | None, data)

        agent_versions = _parse_agent_versions(d.pop("agent_versions"))


        managed_agents_agent_version_list_response = cls(
            agent_versions=agent_versions,
        )


        managed_agents_agent_version_list_response.additional_properties = d
        return managed_agents_agent_version_list_response

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
