from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_memory_store import ManagedAgentsMemoryStore





T = TypeVar("T", bound="ManagedAgentsMemoryStoreListResponse")



@_attrs_define
class ManagedAgentsMemoryStoreListResponse:
    """ The memory stores in the calling organization, newest first.

        Example:
            {'memory_stores': [{'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'archived_at': '2026-02-18T09:30:00Z',
                'created_at': '2026-02-18T09:30:00Z', 'created_by': 'example', 'description': 'example', 'memory_count': 1,
                'memory_store_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'name': 'example-name', 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'origin': 'curated', 'revision': 1, 'slug': 'example', 'status':
                'active', 'total_bytes': 1, 'updated_at': '2026-02-18T09:30:00Z'}]}

        Attributes:
            memory_stores (list[ManagedAgentsMemoryStore] | None): Memory stores in the organization, newest first.
     """

    memory_stores: list[ManagedAgentsMemoryStore] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_memory_store import ManagedAgentsMemoryStore # noqa: PLC0415
        memory_stores: list[dict[str, Any]] | None
        if isinstance(self.memory_stores, list):
            memory_stores = []
            for memory_stores_type_0_item_data in self.memory_stores:
                memory_stores_type_0_item = memory_stores_type_0_item_data.to_dict()
                memory_stores.append(memory_stores_type_0_item)


        else:
            memory_stores = self.memory_stores


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "memory_stores": memory_stores,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_memory_store import ManagedAgentsMemoryStore # noqa: PLC0415
        d = dict(src_dict)
        def _parse_memory_stores(data: object) -> list[ManagedAgentsMemoryStore] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                memory_stores_type_0 = []
                _memory_stores_type_0 = data
                for memory_stores_type_0_item_data in (_memory_stores_type_0):
                    memory_stores_type_0_item = ManagedAgentsMemoryStore.from_dict(memory_stores_type_0_item_data)



                    memory_stores_type_0.append(memory_stores_type_0_item)

                return memory_stores_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsMemoryStore] | None, data)

        memory_stores = _parse_memory_stores(d.pop("memory_stores"))


        managed_agents_memory_store_list_response = cls(
            memory_stores=memory_stores,
        )


        managed_agents_memory_store_list_response.additional_properties = d
        return managed_agents_memory_store_list_response

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
