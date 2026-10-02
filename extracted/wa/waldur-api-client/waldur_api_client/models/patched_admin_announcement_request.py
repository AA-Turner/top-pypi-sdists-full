import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.admin_announcement_type_enum import AdminAnnouncementTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedAdminAnnouncementRequest")


@_attrs_define
class PatchedAdminAnnouncementRequest:
    """
    Attributes:
        description (Union[Unset, str]):
        active_from (Union[Unset, datetime.datetime]):
        active_to (Union[Unset, datetime.datetime]):
        type_ (Union[Unset, AdminAnnouncementTypeEnum]):
    """

    description: Union[Unset, str] = UNSET
    active_from: Union[Unset, datetime.datetime] = UNSET
    active_to: Union[Unset, datetime.datetime] = UNSET
    type_: Union[Unset, AdminAnnouncementTypeEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        active_from: Union[Unset, str] = UNSET
        if not isinstance(self.active_from, Unset):
            active_from = self.active_from.isoformat()

        active_to: Union[Unset, str] = UNSET
        if not isinstance(self.active_to, Unset):
            active_to = self.active_to.isoformat()

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if active_from is not UNSET:
            field_dict["active_from"] = active_from
        if active_to is not UNSET:
            field_dict["active_to"] = active_to
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description", UNSET)

        _active_from = d.pop("active_from", UNSET)
        active_from: Union[Unset, datetime.datetime]
        if isinstance(_active_from, Unset):
            active_from = UNSET
        else:
            active_from = isoparse(_active_from)

        _active_to = d.pop("active_to", UNSET)
        active_to: Union[Unset, datetime.datetime]
        if isinstance(_active_to, Unset):
            active_to = UNSET
        else:
            active_to = isoparse(_active_to)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, AdminAnnouncementTypeEnum]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = AdminAnnouncementTypeEnum(_type_)

        patched_admin_announcement_request = cls(
            description=description,
            active_from=active_from,
            active_to=active_to,
            type_=type_,
        )

        patched_admin_announcement_request.additional_properties = d
        return patched_admin_announcement_request

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
