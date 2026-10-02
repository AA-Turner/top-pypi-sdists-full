from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_reflection import ManagedAgentsReflection





T = TypeVar("T", bound="ManagedAgentsReflectionListResponse")



@_attrs_define
class ManagedAgentsReflectionListResponse:
    """ Memory consolidation runs, newest first.

        Example:
            {'reflections': [{'added_count': 1, 'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'base_revision': 1, 'created_at': '2026-02-18T09:30:00Z',
                'digest_count': 1, 'driver_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'ended_at':
                '2026-02-18T09:30:00Z', 'error_message': 'example', 'error_type': 'example', 'input_session_ids': ['example'],
                'instructions': 'example', 'memory_store_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'merged_count': 1,
                'model': 'example', 'model_ref_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'reflection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'retired_count': 1, 'status': 'pending', 'trigger_window': 'example', 'triggered_by': 'schedule', 'updated_at':
                '2026-02-18T09:30:00Z', 'updated_count': 1}]}

        Attributes:
            reflections (list[ManagedAgentsReflection] | None): Memory consolidation runs, newest first.
     """

    reflections: list[ManagedAgentsReflection] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_reflection import ManagedAgentsReflection # noqa: PLC0415
        reflections: list[dict[str, Any]] | None
        if isinstance(self.reflections, list):
            reflections = []
            for reflections_type_0_item_data in self.reflections:
                reflections_type_0_item = reflections_type_0_item_data.to_dict()
                reflections.append(reflections_type_0_item)


        else:
            reflections = self.reflections


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "reflections": reflections,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_reflection import ManagedAgentsReflection # noqa: PLC0415
        d = dict(src_dict)
        def _parse_reflections(data: object) -> list[ManagedAgentsReflection] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                reflections_type_0 = []
                _reflections_type_0 = data
                for reflections_type_0_item_data in (_reflections_type_0):
                    reflections_type_0_item = ManagedAgentsReflection.from_dict(reflections_type_0_item_data)



                    reflections_type_0.append(reflections_type_0_item)

                return reflections_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsReflection] | None, data)

        reflections = _parse_reflections(d.pop("reflections"))


        managed_agents_reflection_list_response = cls(
            reflections=reflections,
        )


        managed_agents_reflection_list_response.additional_properties = d
        return managed_agents_reflection_list_response

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
