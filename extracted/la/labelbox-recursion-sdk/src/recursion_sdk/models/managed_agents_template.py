from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_agent_template_definition import ManagedAgentsAgentTemplateDefinition





T = TypeVar("T", bound="ManagedAgentsTemplate")



@_attrs_define
class ManagedAgentsTemplate:
    """ One startup-validated static agent template; reading it never creates or mutates an agent.

        Example:
            {'category': 'example', 'definition': {'built_in_integrations': [{'connection_id':
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
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            category (str): Presentation category grouping related agent templates.
            definition (ManagedAgentsAgentTemplateDefinition): Request body for creating an agent: its system prompt, model,
                tool surface, and default vault grants. Sessions snapshot the agent version at start, so later edits do not
                change a running session. Example: {'built_in_integrations': [{'connection_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'tools': ['example']}], 'default_credential_refs': [{'credential_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}],
                'default_project_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'default_rubric': 'example', 'default_vault_ids':
                ['example'], 'description': 'example', 'disabled_integration_mcp_providers': ['example'],
                'max_concurrent_sessions': 1, 'mcp_servers': [{'key': 'example'}], 'metadata': {'key': 'example'}, 'model':
                'example', 'model_config': {'max_tokens': 1, 'provider_params': {'key': 'example'}, 'reasoning_effort':
                'example', 'temperature': 1.5, 'top_p': 1.5}, 'multiagent': {'key': 'example'}, 'name': 'example-name',
                'nativeIntegrations': [{'connectionId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'permission': 'example',
                'resources': ['example']}], 'skills': [{'key': 'example'}], 'system': 'example', 'toolsets': [{'type':
                'evaluation'}], 'web_search_enabled': True}.
            purpose (str): Concise explanation of the work this template is designed to perform.
            template_id (str): Stable catalog key used to select and track this template.
     """

    category: str
    definition: ManagedAgentsAgentTemplateDefinition
    purpose: str
    template_id: str





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_agent_template_definition import ManagedAgentsAgentTemplateDefinition # noqa: PLC0415
        category = self.category

        definition = self.definition.to_dict()

        purpose = self.purpose

        template_id = self.template_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "category": category,
            "definition": definition,
            "purpose": purpose,
            "template_id": template_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_agent_template_definition import ManagedAgentsAgentTemplateDefinition # noqa: PLC0415
        d = dict(src_dict)
        category = d.pop("category")

        definition = ManagedAgentsAgentTemplateDefinition.from_dict(d.pop("definition"))




        purpose = d.pop("purpose")

        template_id = d.pop("template_id")

        managed_agents_template = cls(
            category=category,
            definition=definition,
            purpose=purpose,
            template_id=template_id,
        )

        return managed_agents_template

