from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_definition_response_status import ManagedAgentsAutomationDefinitionResponseStatus
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_automation_git_hub_trigger import ManagedAgentsAutomationGitHubTrigger
  from ..models.managed_agents_automation_literal_prompt import ManagedAgentsAutomationLiteralPrompt
  from ..models.managed_agents_automation_slack_trigger import ManagedAgentsAutomationSlackTrigger
  from ..models.managed_agents_canonical_automation_run_defaults import ManagedAgentsCanonicalAutomationRunDefaults
  from ..models.managed_agents_httpapi_automation_schedule_trigger import ManagedAgentsHttpapiAutomationScheduleTrigger
  from ..models.managed_agents_httpapi_automation_webhook_trigger import ManagedAgentsHttpapiAutomationWebhookTrigger





T = TypeVar("T", bound="ManagedAgentsAutomationDefinitionResponse")



@_attrs_define
class ManagedAgentsAutomationDefinitionResponse:
    """ Full round-trippable canonical automation aggregate.

        Example:
            {'agentId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agentVersionId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'automationId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'createdAt': '2026-02-18T09:30:00Z', 'displayName':
                'example', 'environmentId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'initialPrompt': {'text': 'example', 'type':
                'literal'}, 'revision': 1, 'runDefaults': {'credentialRefs': [{'credentialId': 'example', 'vaultId':
                'example'}], 'memoryStores': [{'access': 'read_only', 'instructions': 'example', 'memoryStoreId': 'example'}],
                'metadata': {'key': 'example'}, 'resources': [{'fileId': 'example', 'mountPath': 'example'}], 'vaultIds':
                ['example']}, 'status': 'paused', 'triggers': [{'enabled': True, 'schedule': {'catchupWindowSeconds': 10,
                'cron': 'example', 'endAt': '2026-02-18T09:30:00Z', 'jitterSeconds': 1, 'overlapPolicy': 'skip', 'startAt':
                '2026-02-18T09:30:00Z', 'timezone': 'example'}, 'triggerId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type':
                'schedule'}], 'updatedAt': '2026-02-18T09:30:00Z'}

        Attributes:
            agent_id (UUID): Managed agent selected by this automation.
            agent_version_id (UUID): Immutable agent version pinned for all admitted runs.
            automation_id (UUID): Stable canonical automation identifier.
            created_at (datetime.datetime): Time the automation was created.
            display_name (str): Human-readable automation name.
            environment_id (UUID): Execution environment selected for admitted sessions.
            initial_prompt (ManagedAgentsAutomationLiteralPrompt): Literal initial prompt frozen onto each admitted
                automation run. Example: {'text': 'example', 'type': 'literal'}.
            revision (int): Monotonic aggregate revision represented by the response ETag.
            run_defaults (ManagedAgentsCanonicalAutomationRunDefaults): Session metadata, credential grants, files and
                memory applied to every trigger and manual admission. Example: {'credentialRefs': [{'credentialId': 'example',
                'vaultId': 'example'}], 'memoryStores': [{'access': 'read_only', 'instructions': 'example', 'memoryStoreId':
                'example'}], 'metadata': {'key': 'example'}, 'resources': [{'fileId': 'example', 'mountPath': 'example'}],
                'vaultIds': ['example']}.
            status (ManagedAgentsAutomationDefinitionResponseStatus): Lifecycle state. New automations start paused.
            triggers (list[ManagedAgentsAutomationGitHubTrigger | ManagedAgentsAutomationSlackTrigger |
                ManagedAgentsHttpapiAutomationScheduleTrigger | ManagedAgentsHttpapiAutomationWebhookTrigger]): Complete ordered
                trigger set.
            updated_at (datetime.datetime): Time the aggregate was last changed.
     """

    agent_id: UUID
    agent_version_id: UUID
    automation_id: UUID
    created_at: datetime.datetime
    display_name: str
    environment_id: UUID
    initial_prompt: ManagedAgentsAutomationLiteralPrompt
    revision: int
    run_defaults: ManagedAgentsCanonicalAutomationRunDefaults
    status: ManagedAgentsAutomationDefinitionResponseStatus
    triggers: list[ManagedAgentsAutomationGitHubTrigger | ManagedAgentsAutomationSlackTrigger | ManagedAgentsHttpapiAutomationScheduleTrigger | ManagedAgentsHttpapiAutomationWebhookTrigger]
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_git_hub_trigger import ManagedAgentsAutomationGitHubTrigger # noqa: PLC0415
        from ..models.managed_agents_automation_literal_prompt import ManagedAgentsAutomationLiteralPrompt # noqa: PLC0415
        from ..models.managed_agents_automation_slack_trigger import ManagedAgentsAutomationSlackTrigger # noqa: PLC0415
        from ..models.managed_agents_canonical_automation_run_defaults import ManagedAgentsCanonicalAutomationRunDefaults # noqa: PLC0415
        from ..models.managed_agents_httpapi_automation_schedule_trigger import ManagedAgentsHttpapiAutomationScheduleTrigger # noqa: PLC0415
        from ..models.managed_agents_httpapi_automation_webhook_trigger import ManagedAgentsHttpapiAutomationWebhookTrigger # noqa: PLC0415
        agent_id = str(self.agent_id)

        agent_version_id = str(self.agent_version_id)

        automation_id = str(self.automation_id)

        created_at = self.created_at.isoformat()

        display_name = self.display_name

        environment_id = str(self.environment_id)

        initial_prompt = self.initial_prompt.to_dict()

        revision = self.revision

        run_defaults = self.run_defaults.to_dict()

        status = self.status.value

        triggers = []
        for triggers_item_data in self.triggers:
            triggers_item: dict[str, Any]
            if isinstance(triggers_item_data, ManagedAgentsHttpapiAutomationScheduleTrigger):
                triggers_item = triggers_item_data.to_dict()
            elif isinstance(triggers_item_data, ManagedAgentsAutomationSlackTrigger):
                triggers_item = triggers_item_data.to_dict()
            elif isinstance(triggers_item_data, ManagedAgentsAutomationGitHubTrigger):
                triggers_item = triggers_item_data.to_dict()
            else:
                triggers_item = triggers_item_data.to_dict()

            triggers.append(triggers_item)



        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agentId": agent_id,
            "agentVersionId": agent_version_id,
            "automationId": automation_id,
            "createdAt": created_at,
            "displayName": display_name,
            "environmentId": environment_id,
            "initialPrompt": initial_prompt,
            "revision": revision,
            "runDefaults": run_defaults,
            "status": status,
            "triggers": triggers,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_git_hub_trigger import ManagedAgentsAutomationGitHubTrigger # noqa: PLC0415
        from ..models.managed_agents_automation_literal_prompt import ManagedAgentsAutomationLiteralPrompt # noqa: PLC0415
        from ..models.managed_agents_automation_slack_trigger import ManagedAgentsAutomationSlackTrigger # noqa: PLC0415
        from ..models.managed_agents_canonical_automation_run_defaults import ManagedAgentsCanonicalAutomationRunDefaults # noqa: PLC0415
        from ..models.managed_agents_httpapi_automation_schedule_trigger import ManagedAgentsHttpapiAutomationScheduleTrigger # noqa: PLC0415
        from ..models.managed_agents_httpapi_automation_webhook_trigger import ManagedAgentsHttpapiAutomationWebhookTrigger # noqa: PLC0415
        d = dict(src_dict)
        agent_id = UUID(d.pop("agentId"))




        agent_version_id = UUID(d.pop("agentVersionId"))




        automation_id = UUID(d.pop("automationId"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        display_name = d.pop("displayName")

        environment_id = UUID(d.pop("environmentId"))




        initial_prompt = ManagedAgentsAutomationLiteralPrompt.from_dict(d.pop("initialPrompt"))




        revision = d.pop("revision")

        run_defaults = ManagedAgentsCanonicalAutomationRunDefaults.from_dict(d.pop("runDefaults"))




        status = ManagedAgentsAutomationDefinitionResponseStatus(d.pop("status"))




        triggers = []
        _triggers = d.pop("triggers")
        for triggers_item_data in (_triggers):
            def _parse_triggers_item(data: object) -> ManagedAgentsAutomationGitHubTrigger | ManagedAgentsAutomationSlackTrigger | ManagedAgentsHttpapiAutomationScheduleTrigger | ManagedAgentsHttpapiAutomationWebhookTrigger:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_managed_agents_canonical_automation_trigger_type_0 = ManagedAgentsHttpapiAutomationScheduleTrigger.from_dict(data)



                    return componentsschemas_managed_agents_canonical_automation_trigger_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_managed_agents_canonical_automation_trigger_type_1 = ManagedAgentsAutomationSlackTrigger.from_dict(data)



                    return componentsschemas_managed_agents_canonical_automation_trigger_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_managed_agents_canonical_automation_trigger_type_2 = ManagedAgentsAutomationGitHubTrigger.from_dict(data)



                    return componentsschemas_managed_agents_canonical_automation_trigger_type_2
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_managed_agents_canonical_automation_trigger_type_3 = ManagedAgentsHttpapiAutomationWebhookTrigger.from_dict(data)



                return componentsschemas_managed_agents_canonical_automation_trigger_type_3

            triggers_item = _parse_triggers_item(triggers_item_data)

            triggers.append(triggers_item)


        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        managed_agents_automation_definition_response = cls(
            agent_id=agent_id,
            agent_version_id=agent_version_id,
            automation_id=automation_id,
            created_at=created_at,
            display_name=display_name,
            environment_id=environment_id,
            initial_prompt=initial_prompt,
            revision=revision,
            run_defaults=run_defaults,
            status=status,
            triggers=triggers,
            updated_at=updated_at,
        )

        return managed_agents_automation_definition_response

