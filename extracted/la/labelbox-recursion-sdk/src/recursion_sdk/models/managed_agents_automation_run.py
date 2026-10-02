from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_run_status import ManagedAgentsAutomationRunStatus
from ..models.managed_agents_automation_run_trigger_type import ManagedAgentsAutomationRunTriggerType
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_automation_run_error import ManagedAgentsAutomationRunError
  from ..models.managed_agents_automation_run_snapshot import ManagedAgentsAutomationRunSnapshot





T = TypeVar("T", bound="ManagedAgentsAutomationRun")



@_attrs_define
class ManagedAgentsAutomationRun:
    """ One recorded attempt to start a managed-agent session from an automation schedule. Records session creation, not the
    session's eventual outcome.

        Example:
            {'automation_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at': '2026-02-18T09:30:00Z', 'error':
                {'code': 'example', 'field': 'example', 'message': 'example', 'resource_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'retryable': True}, 'occurrence_at': '2026-02-18T09:30:00Z',
                'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'snapshot': {'agent_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'credential_refs': [{'credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'cron': 'example', 'environment_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'initial_message_digest': 'example', 'schedule_version': 1, 'timezone':
                'example', 'vault_ids': ['example']}, 'started_at': '2026-02-18T09:30:00Z', 'status': 'pending', 'trigger_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'trigger_type': 'schedule'}

        Attributes:
            automation_id (str): Automation this run belongs to.
            created_at (datetime.datetime): Server-assigned RFC 3339 creation timestamp.
            organization_id (str): Organization that owns the run, resolved from the authenticated request scope.
            run_id (str): Server-assigned run identifier.
            snapshot (ManagedAgentsAutomationRunSnapshot): The automation's configuration frozen at the instant a run fired.
                Example: {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'credential_refs': [{'credential_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'cron': 'example',
                'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'initial_message_digest': 'example',
                'schedule_version': 1, 'timezone': 'example', 'vault_ids': ['example']}.
            started_at (datetime.datetime): When the attempt was made.
            status (ManagedAgentsAutomationRunStatus): Whether the admitted attempt is still resolving, created a session,
                or failed to create one. Native scheduling skips are reported as trigger counters.
            trigger_id (str): Trigger that fired this run.
            trigger_type (ManagedAgentsAutomationRunTriggerType): Schedule trigger that fired the run. Manual and webhook
                dispatch expose sessions through their existing APIs.
            error (ManagedAgentsAutomationRunError | Unset): Why one automation run did not create a session. Example:
                {'code': 'example', 'field': 'example', 'message': 'example', 'resource_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'retryable': True}.
            occurrence_at (datetime.datetime | Unset): The scheduled instant this run answers, without jitter.
            session_id (str | Unset): Session created by this run. Present only when status is created.
     """

    automation_id: str
    created_at: datetime.datetime
    organization_id: str
    run_id: str
    snapshot: ManagedAgentsAutomationRunSnapshot
    started_at: datetime.datetime
    status: ManagedAgentsAutomationRunStatus
    trigger_id: str
    trigger_type: ManagedAgentsAutomationRunTriggerType
    error: ManagedAgentsAutomationRunError | Unset = UNSET
    occurrence_at: datetime.datetime | Unset = UNSET
    session_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_run_error import ManagedAgentsAutomationRunError # noqa: PLC0415
        from ..models.managed_agents_automation_run_snapshot import ManagedAgentsAutomationRunSnapshot # noqa: PLC0415
        automation_id = self.automation_id

        created_at = self.created_at.isoformat()

        organization_id = self.organization_id

        run_id = self.run_id

        snapshot = self.snapshot.to_dict()

        started_at = self.started_at.isoformat()

        status = self.status.value

        trigger_id = self.trigger_id

        trigger_type = self.trigger_type.value

        error: dict[str, Any] | Unset = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        occurrence_at: str | Unset = UNSET
        if not isinstance(self.occurrence_at, Unset):
            occurrence_at = self.occurrence_at.isoformat()

        session_id = self.session_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "automation_id": automation_id,
            "created_at": created_at,
            "organization_id": organization_id,
            "run_id": run_id,
            "snapshot": snapshot,
            "started_at": started_at,
            "status": status,
            "trigger_id": trigger_id,
            "trigger_type": trigger_type,
        })
        if error is not UNSET:
            field_dict["error"] = error
        if occurrence_at is not UNSET:
            field_dict["occurrence_at"] = occurrence_at
        if session_id is not UNSET:
            field_dict["session_id"] = session_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_run_error import ManagedAgentsAutomationRunError # noqa: PLC0415
        from ..models.managed_agents_automation_run_snapshot import ManagedAgentsAutomationRunSnapshot # noqa: PLC0415
        d = dict(src_dict)
        automation_id = d.pop("automation_id")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        organization_id = d.pop("organization_id")

        run_id = d.pop("run_id")

        snapshot = ManagedAgentsAutomationRunSnapshot.from_dict(d.pop("snapshot"))




        started_at = datetime.datetime.fromisoformat(d.pop("started_at"))




        status = ManagedAgentsAutomationRunStatus(d.pop("status"))




        trigger_id = d.pop("trigger_id")

        trigger_type = ManagedAgentsAutomationRunTriggerType(d.pop("trigger_type"))




        _error = d.pop("error", UNSET)
        error: ManagedAgentsAutomationRunError | Unset
        if isinstance(_error,  Unset):
            error = UNSET
        else:
            error = ManagedAgentsAutomationRunError.from_dict(_error)




        _occurrence_at = d.pop("occurrence_at", UNSET)
        occurrence_at: datetime.datetime | Unset
        if isinstance(_occurrence_at,  Unset):
            occurrence_at = UNSET
        else:
            occurrence_at = datetime.datetime.fromisoformat(_occurrence_at)




        session_id = d.pop("session_id", UNSET)

        managed_agents_automation_run = cls(
            automation_id=automation_id,
            created_at=created_at,
            organization_id=organization_id,
            run_id=run_id,
            snapshot=snapshot,
            started_at=started_at,
            status=status,
            trigger_id=trigger_id,
            trigger_type=trigger_type,
            error=error,
            occurrence_at=occurrence_at,
            session_id=session_id,
        )


        managed_agents_automation_run.additional_properties = d
        return managed_agents_automation_run

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
