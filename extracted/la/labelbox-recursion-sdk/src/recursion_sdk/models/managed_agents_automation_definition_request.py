from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.managed_agents_automation_git_hub_trigger_request import ManagedAgentsAutomationGitHubTriggerRequest
  from ..models.managed_agents_automation_literal_prompt import ManagedAgentsAutomationLiteralPrompt
  from ..models.managed_agents_automation_slack_trigger_request import ManagedAgentsAutomationSlackTriggerRequest
  from ..models.managed_agents_canonical_automation_run_defaults_request import ManagedAgentsCanonicalAutomationRunDefaultsRequest
  from ..models.managed_agents_httpapi_automation_schedule_trigger_request import ManagedAgentsHttpapiAutomationScheduleTriggerRequest
  from ..models.managed_agents_httpapi_automation_webhook_trigger_request import ManagedAgentsHttpapiAutomationWebhookTriggerRequest





T = TypeVar("T", bound="ManagedAgentsAutomationDefinitionRequest")



@_attrs_define
class ManagedAgentsAutomationDefinitionRequest:
    """ Complete writable shape for creating or replacing a canonical automation.

        Example:
            {'agentId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agentVersionId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'displayName': 'example', 'environmentId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'initialPrompt': {'text':
                'example', 'type': 'literal'}, 'runDefaults': {'credentialRefs': [{'credentialId': 'example', 'vaultId':
                'example'}], 'memoryStores': [{'access': 'read_only', 'instructions': 'example', 'memoryStoreId': 'example'}],
                'metadata': {'key': 'example'}, 'resources': [{'fileId': 'example', 'mountPath': 'example'}], 'vaultIds':
                ['example']}, 'triggers': [{'enabled': True, 'schedule': {'catchupWindowSeconds': 10, 'cron': 'example',
                'endAt': '2026-02-18T09:30:00Z', 'jitterSeconds': 1, 'overlapPolicy': 'skip', 'startAt': '2026-02-18T09:30:00Z',
                'timezone': 'example'}, 'triggerId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'schedule'}]}

        Attributes:
            agent_id (UUID): Managed agent selected by this automation.
            agent_version_id (UUID): Immutable agent version pinned for all admitted runs.
            display_name (str): Human-readable automation name.
            environment_id (UUID): Execution environment selected for admitted sessions.
            initial_prompt (ManagedAgentsAutomationLiteralPrompt): Literal initial prompt frozen onto each admitted
                automation run. Example: {'text': 'example', 'type': 'literal'}.
            run_defaults (ManagedAgentsCanonicalAutomationRunDefaultsRequest): Session metadata, credential grants, files
                and memory applied to every trigger and manual admission. Example: {'credentialRefs': [{'credentialId':
                'example', 'vaultId': 'example'}], 'memoryStores': [{'access': 'read_only', 'instructions': 'example',
                'memoryStoreId': 'example'}], 'metadata': {'key': 'example'}, 'resources': [{'fileId': 'example', 'mountPath':
                'example'}], 'vaultIds': ['example']}.
            triggers (list[ManagedAgentsAutomationGitHubTriggerRequest | ManagedAgentsAutomationSlackTriggerRequest |
                ManagedAgentsHttpapiAutomationScheduleTriggerRequest | ManagedAgentsHttpapiAutomationWebhookTriggerRequest]):
                Complete trigger set for this automation aggregate.
     """

    agent_id: UUID
    agent_version_id: UUID
    display_name: str
    environment_id: UUID
    initial_prompt: ManagedAgentsAutomationLiteralPrompt
    run_defaults: ManagedAgentsCanonicalAutomationRunDefaultsRequest
    triggers: list[ManagedAgentsAutomationGitHubTriggerRequest | ManagedAgentsAutomationSlackTriggerRequest | ManagedAgentsHttpapiAutomationScheduleTriggerRequest | ManagedAgentsHttpapiAutomationWebhookTriggerRequest]





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_git_hub_trigger_request import ManagedAgentsAutomationGitHubTriggerRequest # noqa: PLC0415
        from ..models.managed_agents_automation_literal_prompt import ManagedAgentsAutomationLiteralPrompt # noqa: PLC0415
        from ..models.managed_agents_automation_slack_trigger_request import ManagedAgentsAutomationSlackTriggerRequest # noqa: PLC0415
        from ..models.managed_agents_canonical_automation_run_defaults_request import ManagedAgentsCanonicalAutomationRunDefaultsRequest # noqa: PLC0415
        from ..models.managed_agents_httpapi_automation_schedule_trigger_request import ManagedAgentsHttpapiAutomationScheduleTriggerRequest # noqa: PLC0415
        from ..models.managed_agents_httpapi_automation_webhook_trigger_request import ManagedAgentsHttpapiAutomationWebhookTriggerRequest # noqa: PLC0415
        agent_id = str(self.agent_id)

        agent_version_id = str(self.agent_version_id)

        display_name = self.display_name

        environment_id = str(self.environment_id)

        initial_prompt = self.initial_prompt.to_dict()

        run_defaults = self.run_defaults.to_dict()

        triggers = []
        for triggers_item_data in self.triggers:
            triggers_item: dict[str, Any]
            if isinstance(triggers_item_data, ManagedAgentsHttpapiAutomationScheduleTriggerRequest):
                triggers_item = triggers_item_data.to_dict()
            elif isinstance(triggers_item_data, ManagedAgentsAutomationSlackTriggerRequest):
                triggers_item = triggers_item_data.to_dict()
            elif isinstance(triggers_item_data, ManagedAgentsAutomationGitHubTriggerRequest):
                triggers_item = triggers_item_data.to_dict()
            else:
                triggers_item = triggers_item_data.to_dict()

            triggers.append(triggers_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agentId": agent_id,
            "agentVersionId": agent_version_id,
            "displayName": display_name,
            "environmentId": environment_id,
            "initialPrompt": initial_prompt,
            "runDefaults": run_defaults,
            "triggers": triggers,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_git_hub_trigger_request import ManagedAgentsAutomationGitHubTriggerRequest # noqa: PLC0415
        from ..models.managed_agents_automation_literal_prompt import ManagedAgentsAutomationLiteralPrompt # noqa: PLC0415
        from ..models.managed_agents_automation_slack_trigger_request import ManagedAgentsAutomationSlackTriggerRequest # noqa: PLC0415
        from ..models.managed_agents_canonical_automation_run_defaults_request import ManagedAgentsCanonicalAutomationRunDefaultsRequest # noqa: PLC0415
        from ..models.managed_agents_httpapi_automation_schedule_trigger_request import ManagedAgentsHttpapiAutomationScheduleTriggerRequest # noqa: PLC0415
        from ..models.managed_agents_httpapi_automation_webhook_trigger_request import ManagedAgentsHttpapiAutomationWebhookTriggerRequest # noqa: PLC0415
        d = dict(src_dict)
        agent_id = UUID(d.pop("agentId"))




        agent_version_id = UUID(d.pop("agentVersionId"))




        display_name = d.pop("displayName")

        environment_id = UUID(d.pop("environmentId"))




        initial_prompt = ManagedAgentsAutomationLiteralPrompt.from_dict(d.pop("initialPrompt"))




        run_defaults = ManagedAgentsCanonicalAutomationRunDefaultsRequest.from_dict(d.pop("runDefaults"))




        triggers = []
        _triggers = d.pop("triggers")
        for triggers_item_data in (_triggers):
            def _parse_triggers_item(data: object) -> ManagedAgentsAutomationGitHubTriggerRequest | ManagedAgentsAutomationSlackTriggerRequest | ManagedAgentsHttpapiAutomationScheduleTriggerRequest | ManagedAgentsHttpapiAutomationWebhookTriggerRequest:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_managed_agents_canonical_automation_trigger_request_type_0 = ManagedAgentsHttpapiAutomationScheduleTriggerRequest.from_dict(data)



                    return componentsschemas_managed_agents_canonical_automation_trigger_request_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_managed_agents_canonical_automation_trigger_request_type_1 = ManagedAgentsAutomationSlackTriggerRequest.from_dict(data)



                    return componentsschemas_managed_agents_canonical_automation_trigger_request_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_managed_agents_canonical_automation_trigger_request_type_2 = ManagedAgentsAutomationGitHubTriggerRequest.from_dict(data)



                    return componentsschemas_managed_agents_canonical_automation_trigger_request_type_2
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_managed_agents_canonical_automation_trigger_request_type_3 = ManagedAgentsHttpapiAutomationWebhookTriggerRequest.from_dict(data)



                return componentsschemas_managed_agents_canonical_automation_trigger_request_type_3

            triggers_item = _parse_triggers_item(triggers_item_data)

            triggers.append(triggers_item)


        managed_agents_automation_definition_request = cls(
            agent_id=agent_id,
            agent_version_id=agent_version_id,
            display_name=display_name,
            environment_id=environment_id,
            initial_prompt=initial_prompt,
            run_defaults=run_defaults,
            triggers=triggers,
        )

        return managed_agents_automation_definition_request

