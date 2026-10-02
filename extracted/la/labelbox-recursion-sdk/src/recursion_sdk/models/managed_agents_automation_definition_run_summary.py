from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_definition_run_summary_status import ManagedAgentsAutomationDefinitionRunSummaryStatus
from ..models.managed_agents_automation_definition_run_summary_trigger_type import ManagedAgentsAutomationDefinitionRunSummaryTriggerType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_automation_definition_run_error_response import ManagedAgentsAutomationDefinitionRunErrorResponse





T = TypeVar("T", bound="ManagedAgentsAutomationDefinitionRunSummary")



@_attrs_define
class ManagedAgentsAutomationDefinitionRunSummary:
    """ A canonical automation run without its frozen snapshots; read the member for those.

        Example:
            {'automationId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'automationRunId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'completedAt': '2026-02-18T09:30:00Z', 'createdAt':
                '2026-02-18T09:30:00Z', 'error': {'code': 'example', 'field': 'example', 'message': 'example', 'resourceId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'retryable': True}, 'eventSourceId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'occurrenceAt': '2026-02-18T09:30:00Z', 'providerDeliveryId': 'example',
                'sessionId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'pending', 'statusUrl': 'example', 'triggerId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'triggerIncarnation': 1, 'triggerType': 'manual', 'updatedAt':
                '2026-02-18T09:30:00Z'}

        Attributes:
            automation_id (UUID): Automation whose frozen configuration admitted the run.
            automation_run_id (UUID): Stable run identifier and asynchronous status handle.
            created_at (datetime.datetime): Time the run was admitted.
            status (ManagedAgentsAutomationDefinitionRunSummaryStatus): Session-creation outcome.
            status_url (str): Canonical member URL for polling this run.
            trigger_type (ManagedAgentsAutomationDefinitionRunSummaryTriggerType): Admission kind.
            updated_at (datetime.datetime): Time the run outcome last changed.
            completed_at (datetime.datetime | Unset): Time session creation succeeded or failed.
            error (ManagedAgentsAutomationDefinitionRunErrorResponse | Unset): Terminal failure that stopped a canonical
                automation run before or during session admission. Example: {'code': 'example', 'field': 'example', 'message':
                'example', 'resourceId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'retryable': True}.
            event_source_id (UUID | Unset): Event source that received the delivery for provider and custom-webhook runs.
            occurrence_at (datetime.datetime | Unset): Schedule occurrence represented by this run.
            provider_delivery_id (str | Unset): Verified provider delivery identity used for deduplication.
            session_id (UUID | Unset): Created managed-agent session. Present only for created runs.
            trigger_id (UUID | Unset): Stored trigger that admitted the run. Absent for manual runs.
            trigger_incarnation (int | Unset): Trigger incarnation frozen at admission. Absent for manual runs.
     """

    automation_id: UUID
    automation_run_id: UUID
    created_at: datetime.datetime
    status: ManagedAgentsAutomationDefinitionRunSummaryStatus
    status_url: str
    trigger_type: ManagedAgentsAutomationDefinitionRunSummaryTriggerType
    updated_at: datetime.datetime
    completed_at: datetime.datetime | Unset = UNSET
    error: ManagedAgentsAutomationDefinitionRunErrorResponse | Unset = UNSET
    event_source_id: UUID | Unset = UNSET
    occurrence_at: datetime.datetime | Unset = UNSET
    provider_delivery_id: str | Unset = UNSET
    session_id: UUID | Unset = UNSET
    trigger_id: UUID | Unset = UNSET
    trigger_incarnation: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_definition_run_error_response import ManagedAgentsAutomationDefinitionRunErrorResponse # noqa: PLC0415
        automation_id = str(self.automation_id)

        automation_run_id = str(self.automation_run_id)

        created_at = self.created_at.isoformat()

        status = self.status.value

        status_url = self.status_url

        trigger_type = self.trigger_type.value

        updated_at = self.updated_at.isoformat()

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        error: dict[str, Any] | Unset = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        event_source_id: str | Unset = UNSET
        if not isinstance(self.event_source_id, Unset):
            event_source_id = str(self.event_source_id)

        occurrence_at: str | Unset = UNSET
        if not isinstance(self.occurrence_at, Unset):
            occurrence_at = self.occurrence_at.isoformat()

        provider_delivery_id = self.provider_delivery_id

        session_id: str | Unset = UNSET
        if not isinstance(self.session_id, Unset):
            session_id = str(self.session_id)

        trigger_id: str | Unset = UNSET
        if not isinstance(self.trigger_id, Unset):
            trigger_id = str(self.trigger_id)

        trigger_incarnation = self.trigger_incarnation


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "automationId": automation_id,
            "automationRunId": automation_run_id,
            "createdAt": created_at,
            "status": status,
            "statusUrl": status_url,
            "triggerType": trigger_type,
            "updatedAt": updated_at,
        })
        if completed_at is not UNSET:
            field_dict["completedAt"] = completed_at
        if error is not UNSET:
            field_dict["error"] = error
        if event_source_id is not UNSET:
            field_dict["eventSourceId"] = event_source_id
        if occurrence_at is not UNSET:
            field_dict["occurrenceAt"] = occurrence_at
        if provider_delivery_id is not UNSET:
            field_dict["providerDeliveryId"] = provider_delivery_id
        if session_id is not UNSET:
            field_dict["sessionId"] = session_id
        if trigger_id is not UNSET:
            field_dict["triggerId"] = trigger_id
        if trigger_incarnation is not UNSET:
            field_dict["triggerIncarnation"] = trigger_incarnation

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_definition_run_error_response import ManagedAgentsAutomationDefinitionRunErrorResponse # noqa: PLC0415
        d = dict(src_dict)
        automation_id = UUID(d.pop("automationId"))




        automation_run_id = UUID(d.pop("automationRunId"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        status = ManagedAgentsAutomationDefinitionRunSummaryStatus(d.pop("status"))




        status_url = d.pop("statusUrl")

        trigger_type = ManagedAgentsAutomationDefinitionRunSummaryTriggerType(d.pop("triggerType"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        _completed_at = d.pop("completedAt", UNSET)
        completed_at: datetime.datetime | Unset
        if isinstance(_completed_at,  Unset):
            completed_at = UNSET
        else:
            completed_at = datetime.datetime.fromisoformat(_completed_at)




        _error = d.pop("error", UNSET)
        error: ManagedAgentsAutomationDefinitionRunErrorResponse | Unset
        if isinstance(_error,  Unset):
            error = UNSET
        else:
            error = ManagedAgentsAutomationDefinitionRunErrorResponse.from_dict(_error)




        _event_source_id = d.pop("eventSourceId", UNSET)
        event_source_id: UUID | Unset
        if isinstance(_event_source_id,  Unset):
            event_source_id = UNSET
        else:
            event_source_id = UUID(_event_source_id)




        _occurrence_at = d.pop("occurrenceAt", UNSET)
        occurrence_at: datetime.datetime | Unset
        if isinstance(_occurrence_at,  Unset):
            occurrence_at = UNSET
        else:
            occurrence_at = datetime.datetime.fromisoformat(_occurrence_at)




        provider_delivery_id = d.pop("providerDeliveryId", UNSET)

        _session_id = d.pop("sessionId", UNSET)
        session_id: UUID | Unset
        if isinstance(_session_id,  Unset):
            session_id = UNSET
        else:
            session_id = UUID(_session_id)




        _trigger_id = d.pop("triggerId", UNSET)
        trigger_id: UUID | Unset
        if isinstance(_trigger_id,  Unset):
            trigger_id = UNSET
        else:
            trigger_id = UUID(_trigger_id)




        trigger_incarnation = d.pop("triggerIncarnation", UNSET)

        managed_agents_automation_definition_run_summary = cls(
            automation_id=automation_id,
            automation_run_id=automation_run_id,
            created_at=created_at,
            status=status,
            status_url=status_url,
            trigger_type=trigger_type,
            updated_at=updated_at,
            completed_at=completed_at,
            error=error,
            event_source_id=event_source_id,
            occurrence_at=occurrence_at,
            provider_delivery_id=provider_delivery_id,
            session_id=session_id,
            trigger_id=trigger_id,
            trigger_incarnation=trigger_incarnation,
        )

        return managed_agents_automation_definition_run_summary

