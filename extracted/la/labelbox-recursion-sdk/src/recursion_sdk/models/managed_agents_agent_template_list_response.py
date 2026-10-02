from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_template import ManagedAgentsTemplate





T = TypeVar("T", bound="ManagedAgentsAgentTemplateListResponse")



@_attrs_define
class ManagedAgentsAgentTemplateListResponse:
    """ Response body of GET /v1/agent-templates: the static startup-validated agent template catalog.

        Example:
            {'agent_templates': [{'category': 'example', 'definition': {'built_in_integrations': [{'connection_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'tools': ['example']}], 'default_credential_refs': [{'credential_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}],
                'default_project_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'default_rubric': 'example', 'default_vault_ids':
                ['example'], 'description': 'example', 'disabled_integration_mcp_providers': ['example'],
                'max_concurrent_sessions': 1, 'mcp_servers': [{'key': 'example'}], 'metadata': {'key': 'example'}, 'model':
                'example', 'model_config': {'max_tokens': 1, 'provider_params': {'key': 'example'}, 'reasoning_effort':
                'example', 'temperature': 1.5, 'top_p': 1.5}, 'multiagent': {'key': 'example'}, 'name': 'example-name',
                'nativeIntegrations': [{'connectionId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'permission': 'example',
                'resources': ['example']}], 'skills': [{'key': 'example'}], 'system': 'example', 'toolsets': [{'type':
                'evaluation'}], 'web_search_enabled': True}, 'purpose': 'example', 'template_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}]}

        Attributes:
            agent_templates (list[ManagedAgentsTemplate]): Stable evaluation-agent templates sorted by template_id.
                Definitions are ordinary createAgent request bodies copied into the create form; reading this catalog never
                creates or mutates an agent.
     """

    agent_templates: list[ManagedAgentsTemplate]





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_template import ManagedAgentsTemplate # noqa: PLC0415
        agent_templates = []
        for agent_templates_item_data in self.agent_templates:
            agent_templates_item = agent_templates_item_data.to_dict()
            agent_templates.append(agent_templates_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_templates": agent_templates,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_template import ManagedAgentsTemplate # noqa: PLC0415
        d = dict(src_dict)
        agent_templates = []
        _agent_templates = d.pop("agent_templates")
        for agent_templates_item_data in (_agent_templates):
            agent_templates_item = ManagedAgentsTemplate.from_dict(agent_templates_item_data)



            agent_templates.append(agent_templates_item)


        managed_agents_agent_template_list_response = cls(
            agent_templates=agent_templates,
        )

        return managed_agents_agent_template_list_response

