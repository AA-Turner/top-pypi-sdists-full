from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.observable_object_type_enum import ObservableObjectTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentQueueRegistrationRequest")


@_attrs_define
class AgentQueueRegistrationRequest:
    """
    Attributes:
        object_types (Union[Unset, list[ObservableObjectTypeEnum]]): List of observable object types to receive. An
            explicit empty list means all types; omitting the field leaves the current filter unchanged.
    """

    object_types: Union[Unset, list[ObservableObjectTypeEnum]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.object_types, Unset):
            object_types = []
            for object_types_item_data in self.object_types:
                object_types_item = object_types_item_data.value
                object_types.append(object_types_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if object_types is not UNSET:
            field_dict["object_types"] = object_types

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        object_types = []
        _object_types = d.pop("object_types", UNSET)
        for object_types_item_data in _object_types or []:
            object_types_item = ObservableObjectTypeEnum(object_types_item_data)

            object_types.append(object_types_item)

        agent_queue_registration_request = cls(
            object_types=object_types,
        )

        agent_queue_registration_request.additional_properties = d
        return agent_queue_registration_request

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
