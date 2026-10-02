import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.admin_announcement_type_enum import AdminAnnouncementTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AdminAnnouncementRequest")


@_attrs_define
class AdminAnnouncementRequest:
    """
    Attributes:
        active_from (datetime.datetime):
        active_to (datetime.datetime):
        description (Union[Unset, str]):
        type_ (Union[Unset, AdminAnnouncementTypeEnum]):
    """

    active_from: datetime.datetime
    active_to: datetime.datetime
    description: Union[Unset, str] = UNSET
    type_: Union[Unset, AdminAnnouncementTypeEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        active_from = self.active_from.isoformat()

        active_to = self.active_to.isoformat()

        description = self.description

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active_from": active_from,
                "active_to": active_to,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        active_from = isoparse(d.pop("active_from"))

        active_to = isoparse(d.pop("active_to"))

        description = d.pop("description", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, AdminAnnouncementTypeEnum]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = AdminAnnouncementTypeEnum(_type_)

        admin_announcement_request = cls(
            active_from=active_from,
            active_to=active_to,
            description=description,
            type_=type_,
        )

        admin_announcement_request.additional_properties = d
        return admin_announcement_request

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
