from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_reflection import ManagedAgentsReflection





T = TypeVar("T", bound="ManagedAgentsMemoryActivityPage")



@_attrs_define
class ManagedAgentsMemoryActivityPage:
    """ An agent's automatic memory activity, including checks with no changes and retrying failures.

        Example:
            {'next_cursor': 'example', 'reflections': [{'added_count': 1, 'agent_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'base_revision': 1, 'created_at': '2026-02-18T09:30:00Z', 'digest_count': 1, 'driver_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'ended_at': '2026-02-18T09:30:00Z', 'error_message': 'example',
                'error_type': 'example', 'input_session_ids': ['example'], 'instructions': 'example', 'memory_store_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'merged_count': 1, 'model': 'example', 'model_ref_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'reflection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'retired_count': 1, 'status': 'pending',
                'trigger_window': 'example', 'triggered_by': 'schedule', 'updated_at': '2026-02-18T09:30:00Z', 'updated_count':
                1}]}

        Attributes:
            reflections (list[ManagedAgentsReflection]): Automatic memory runs, newest first.
            next_cursor (str | Unset): Opaque cursor for the next activity page.
     """

    reflections: list[ManagedAgentsReflection]
    next_cursor: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_reflection import ManagedAgentsReflection # noqa: PLC0415
        reflections = []
        for reflections_item_data in self.reflections:
            reflections_item = reflections_item_data.to_dict()
            reflections.append(reflections_item)



        next_cursor = self.next_cursor


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "reflections": reflections,
        })
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_reflection import ManagedAgentsReflection # noqa: PLC0415
        d = dict(src_dict)
        reflections = []
        _reflections = d.pop("reflections")
        for reflections_item_data in (_reflections):
            reflections_item = ManagedAgentsReflection.from_dict(reflections_item_data)



            reflections.append(reflections_item)


        next_cursor = d.pop("next_cursor", UNSET)

        managed_agents_memory_activity_page = cls(
            reflections=reflections,
            next_cursor=next_cursor,
        )


        managed_agents_memory_activity_page.additional_properties = d
        return managed_agents_memory_activity_page

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
