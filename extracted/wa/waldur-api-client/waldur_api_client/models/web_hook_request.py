from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_groups_enum import EventGroupsEnum
from ..models.event_types_enum import EventTypesEnum
from ..models.web_hook_content_type_enum import WebHookContentTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="WebHookRequest")


@_attrs_define
class WebHookRequest:
    """
    Attributes:
        destination_url (str):
        is_active (Union[Unset, bool]):
        event_types (Union[Unset, list[EventTypesEnum]]):
        event_groups (Union[Unset, list[EventGroupsEnum]]):
        content_type (Union[Unset, WebHookContentTypeEnum]):
    """

    destination_url: str
    is_active: Union[Unset, bool] = UNSET
    event_types: Union[Unset, list[EventTypesEnum]] = UNSET
    event_groups: Union[Unset, list[EventGroupsEnum]] = UNSET
    content_type: Union[Unset, WebHookContentTypeEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        destination_url = self.destination_url

        is_active = self.is_active

        event_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.event_types, Unset):
            event_types = []
            for event_types_item_data in self.event_types:
                event_types_item = event_types_item_data.value
                event_types.append(event_types_item)

        event_groups: Union[Unset, list[str]] = UNSET
        if not isinstance(self.event_groups, Unset):
            event_groups = []
            for event_groups_item_data in self.event_groups:
                event_groups_item = event_groups_item_data.value
                event_groups.append(event_groups_item)

        content_type: Union[Unset, str] = UNSET
        if not isinstance(self.content_type, Unset):
            content_type = self.content_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "destination_url": destination_url,
            }
        )
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if event_types is not UNSET:
            field_dict["event_types"] = event_types
        if event_groups is not UNSET:
            field_dict["event_groups"] = event_groups
        if content_type is not UNSET:
            field_dict["content_type"] = content_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        destination_url = d.pop("destination_url")

        is_active = d.pop("is_active", UNSET)

        event_types = []
        _event_types = d.pop("event_types", UNSET)
        for event_types_item_data in _event_types or []:
            event_types_item = EventTypesEnum(event_types_item_data)

            event_types.append(event_types_item)

        event_groups = []
        _event_groups = d.pop("event_groups", UNSET)
        for event_groups_item_data in _event_groups or []:
            event_groups_item = EventGroupsEnum(event_groups_item_data)

            event_groups.append(event_groups_item)

        _content_type = d.pop("content_type", UNSET)
        content_type: Union[Unset, WebHookContentTypeEnum]
        if isinstance(_content_type, Unset):
            content_type = UNSET
        else:
            content_type = WebHookContentTypeEnum(_content_type)

        web_hook_request = cls(
            destination_url=destination_url,
            is_active=is_active,
            event_types=event_types,
            event_groups=event_groups,
            content_type=content_type,
        )

        web_hook_request.additional_properties = d
        return web_hook_request

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
