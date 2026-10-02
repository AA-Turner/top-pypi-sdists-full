from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_automation_definition_run_summary import ManagedAgentsAutomationDefinitionRunSummary





T = TypeVar("T", bound="ManagedAgentsAutomationDefinitionRunPageResponse")



@_attrs_define
class ManagedAgentsAutomationDefinitionRunPageResponse:
    """ A bounded snapshot-consistent page of canonical automation runs.

        Example:
            {'items': [{'automationId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'automationRunId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'completedAt': '2026-02-18T09:30:00Z', 'createdAt':
                '2026-02-18T09:30:00Z', 'error': {'code': 'example', 'field': 'example', 'message': 'example', 'resourceId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'retryable': True}, 'eventSourceId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'occurrenceAt': '2026-02-18T09:30:00Z', 'providerDeliveryId': 'example',
                'sessionId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'pending', 'statusUrl': 'example', 'triggerId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'triggerIncarnation': 1, 'triggerType': 'manual', 'updatedAt':
                '2026-02-18T09:30:00Z'}], 'nextCursor': 'example', 'total': 1}

        Attributes:
            items (list[ManagedAgentsAutomationDefinitionRunSummary]): Canonical automation runs, newest first.
            next_cursor (None | str): Opaque continuation cursor, or null at the end.
            total (int): Total matching runs at the page's read snapshot.
     """

    items: list[ManagedAgentsAutomationDefinitionRunSummary]
    next_cursor: None | str
    total: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_definition_run_summary import ManagedAgentsAutomationDefinitionRunSummary # noqa: PLC0415
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)



        next_cursor: None | str
        next_cursor = self.next_cursor

        total = self.total


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
            "nextCursor": next_cursor,
            "total": total,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_definition_run_summary import ManagedAgentsAutomationDefinitionRunSummary # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = ManagedAgentsAutomationDefinitionRunSummary.from_dict(items_item_data)



            items.append(items_item)


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))


        total = d.pop("total")

        managed_agents_automation_definition_run_page_response = cls(
            items=items,
            next_cursor=next_cursor,
            total=total,
        )

        return managed_agents_automation_definition_run_page_response

