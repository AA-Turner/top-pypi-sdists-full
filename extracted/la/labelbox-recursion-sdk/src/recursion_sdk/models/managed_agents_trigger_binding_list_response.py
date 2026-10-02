from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_trigger_binding import ManagedAgentsTriggerBinding





T = TypeVar("T", bound="ManagedAgentsTriggerBindingListResponse")



@_attrs_define
class ManagedAgentsTriggerBindingListResponse:
    """ Response body of GET /v1/trigger-bindings. Unpaginated, and scoped to the one connection named by the required
    connection_id query parameter within the calling organization.

        Example:
            {'bindings': [{'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'automation_kind': 'example', 'binding_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'capture_patch': True, 'channel_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'enabled':
                True, 'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'include_drafts': True, 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'owner_key': 'example', 'provider': 'example', 'publish_review': True,
                'repository': 'example', 'repository_id': 1, 'vault_ids': ['example'], 'wake_app_ids': ['example'],
                'wake_event': 'example'}]}

        Attributes:
            bindings (list[ManagedAgentsTriggerBinding] | None): The connection's live bindings, ordered by binding_id.
                Disabled bindings are included; deleted ones are not.
     """

    bindings: list[ManagedAgentsTriggerBinding] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_trigger_binding import ManagedAgentsTriggerBinding # noqa: PLC0415
        bindings: list[dict[str, Any]] | None
        if isinstance(self.bindings, list):
            bindings = []
            for bindings_type_0_item_data in self.bindings:
                bindings_type_0_item = bindings_type_0_item_data.to_dict()
                bindings.append(bindings_type_0_item)


        else:
            bindings = self.bindings


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "bindings": bindings,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_trigger_binding import ManagedAgentsTriggerBinding # noqa: PLC0415
        d = dict(src_dict)
        def _parse_bindings(data: object) -> list[ManagedAgentsTriggerBinding] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                bindings_type_0 = []
                _bindings_type_0 = data
                for bindings_type_0_item_data in (_bindings_type_0):
                    bindings_type_0_item = ManagedAgentsTriggerBinding.from_dict(bindings_type_0_item_data)



                    bindings_type_0.append(bindings_type_0_item)

                return bindings_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsTriggerBinding] | None, data)

        bindings = _parse_bindings(d.pop("bindings"))


        managed_agents_trigger_binding_list_response = cls(
            bindings=bindings,
        )


        managed_agents_trigger_binding_list_response.additional_properties = d
        return managed_agents_trigger_binding_list_response

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
