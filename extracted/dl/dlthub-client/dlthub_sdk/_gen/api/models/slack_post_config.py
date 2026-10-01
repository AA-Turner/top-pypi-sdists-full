from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SlackPostConfig")


@_attrs_define
class SlackPostConfig:
    """Configuration for Slack action

    Attributes:
        destination_ids (list[UUID] | Unset): IDs of notification destinations to deliver to
    """

    destination_ids: list[UUID] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        destination_ids: list[str] | Unset = UNSET
        if not isinstance(self.destination_ids, Unset):
            destination_ids = []
            for destination_ids_item_data in self.destination_ids:
                destination_ids_item = str(destination_ids_item_data)
                destination_ids.append(destination_ids_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if destination_ids is not UNSET:
            field_dict["destination_ids"] = destination_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _destination_ids = d.pop("destination_ids", UNSET)
        destination_ids: list[UUID] | Unset = UNSET
        if _destination_ids is not UNSET:
            destination_ids = []
            for destination_ids_item_data in _destination_ids:
                destination_ids_item = UUID(destination_ids_item_data)

                destination_ids.append(destination_ids_item)

        slack_post_config = cls(
            destination_ids=destination_ids,
        )

        slack_post_config.additional_properties = d
        return slack_post_config

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
