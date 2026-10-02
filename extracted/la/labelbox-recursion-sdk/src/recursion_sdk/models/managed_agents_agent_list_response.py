from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_agent import ManagedAgentsAgent





T = TypeVar("T", bound="ManagedAgentsAgentListResponse")



@_attrs_define
class ManagedAgentsAgentListResponse:
    """ Response body of GET /v1/agents. Unpaginated: the whole organization is returned in one document, so callers need no
    cursor here. Each row is the agent's current mutable definition; its immutable snapshots are listed by GET
    /v1/agents/{agent_id}/versions.

        Example:
            {'agents': [{'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'built_in_integrations': [{'connection_id':
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
                'web_search_enabled': True}]}

        Attributes:
            agents (list[ManagedAgentsAgent] | None): Every agent in the caller's organization, newest first. Null rather
                than an empty array when the organization has no agents. Soft-deleted agents are omitted.
     """

    agents: list[ManagedAgentsAgent] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_agent import ManagedAgentsAgent # noqa: PLC0415
        agents: list[dict[str, Any]] | None
        if isinstance(self.agents, list):
            agents = []
            for agents_type_0_item_data in self.agents:
                agents_type_0_item = agents_type_0_item_data.to_dict()
                agents.append(agents_type_0_item)


        else:
            agents = self.agents


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "agents": agents,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_agent import ManagedAgentsAgent # noqa: PLC0415
        d = dict(src_dict)
        def _parse_agents(data: object) -> list[ManagedAgentsAgent] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                agents_type_0 = []
                _agents_type_0 = data
                for agents_type_0_item_data in (_agents_type_0):
                    agents_type_0_item = ManagedAgentsAgent.from_dict(agents_type_0_item_data)



                    agents_type_0.append(agents_type_0_item)

                return agents_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsAgent] | None, data)

        agents = _parse_agents(d.pop("agents"))


        managed_agents_agent_list_response = cls(
            agents=agents,
        )


        managed_agents_agent_list_response.additional_properties = d
        return managed_agents_agent_list_response

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
