from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_automation_run import ManagedAgentsAutomationRun





T = TypeVar("T", bound="ManagedAgentsAutomationRunListResponse")



@_attrs_define
class ManagedAgentsAutomationRunListResponse:
    """ A page of scheduled automation run records, newest first.

        Example:
            {'automation_runs': [{'automation_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at':
                '2026-02-18T09:30:00Z', 'error': {'code': 'example', 'field': 'example', 'message': 'example', 'resource_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'retryable': True}, 'occurrence_at': '2026-02-18T09:30:00Z',
                'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'snapshot': {'agent_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'credential_refs': [{'credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'cron': 'example', 'environment_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'initial_message_digest': 'example', 'schedule_version': 1, 'timezone':
                'example', 'vault_ids': ['example']}, 'started_at': '2026-02-18T09:30:00Z', 'status': 'pending', 'trigger_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'trigger_type': 'schedule'}], 'next_cursor': 'example'}

        Attributes:
            automation_runs (list[ManagedAgentsAutomationRun] | None): Run records, newest first.
            next_cursor (str | Unset): Opaque cursor for the next page; absent when this is the last page.
     """

    automation_runs: list[ManagedAgentsAutomationRun] | None
    next_cursor: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_run import ManagedAgentsAutomationRun # noqa: PLC0415
        automation_runs: list[dict[str, Any]] | None
        if isinstance(self.automation_runs, list):
            automation_runs = []
            for automation_runs_type_0_item_data in self.automation_runs:
                automation_runs_type_0_item = automation_runs_type_0_item_data.to_dict()
                automation_runs.append(automation_runs_type_0_item)


        else:
            automation_runs = self.automation_runs

        next_cursor = self.next_cursor


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "automation_runs": automation_runs,
        })
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_run import ManagedAgentsAutomationRun # noqa: PLC0415
        d = dict(src_dict)
        def _parse_automation_runs(data: object) -> list[ManagedAgentsAutomationRun] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                automation_runs_type_0 = []
                _automation_runs_type_0 = data
                for automation_runs_type_0_item_data in (_automation_runs_type_0):
                    automation_runs_type_0_item = ManagedAgentsAutomationRun.from_dict(automation_runs_type_0_item_data)



                    automation_runs_type_0.append(automation_runs_type_0_item)

                return automation_runs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsAutomationRun] | None, data)

        automation_runs = _parse_automation_runs(d.pop("automation_runs"))


        next_cursor = d.pop("next_cursor", UNSET)

        managed_agents_automation_run_list_response = cls(
            automation_runs=automation_runs,
            next_cursor=next_cursor,
        )


        managed_agents_automation_run_list_response.additional_properties = d
        return managed_agents_automation_run_list_response

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
