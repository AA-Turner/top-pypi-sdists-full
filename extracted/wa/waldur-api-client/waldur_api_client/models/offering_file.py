import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingFile")


@_attrs_define
class OfferingFile:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        offering (Union[Unset, str]):
        created (Union[Unset, datetime.datetime]):
        file (Union[Unset, str]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    offering: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    file: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        name = self.name

        offering = self.offering

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        file = self.file

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if offering is not UNSET:
            field_dict["offering"] = offering
        if created is not UNSET:
            field_dict["created"] = created
        if file is not UNSET:
            field_dict["file"] = file

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        name = d.pop("name", UNSET)

        offering = d.pop("offering", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        file = d.pop("file", UNSET)

        offering_file = cls(
            url=url,
            uuid=uuid,
            name=name,
            offering=offering,
            created=created,
            file=file,
        )

        offering_file.additional_properties = d
        return offering_file

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
