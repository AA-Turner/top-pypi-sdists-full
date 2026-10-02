import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CleanupResponseItem")


@_attrs_define
class CleanupResponseItem:
    """
    Attributes:
        uuid (UUID):
        name (str):
        offering_name (Union[Unset, str]):
        created (Union[Unset, datetime.datetime]):
        identity_name (Union[Unset, str]):
        state (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
    """

    uuid: UUID
    name: str
    offering_name: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    identity_name: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        offering_name = self.offering_name

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        identity_name = self.identity_name

        state = self.state

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
            }
        )
        if offering_name is not UNSET:
            field_dict["offering__name"] = offering_name
        if created is not UNSET:
            field_dict["created"] = created
        if identity_name is not UNSET:
            field_dict["identity__name"] = identity_name
        if state is not UNSET:
            field_dict["state"] = state
        if modified is not UNSET:
            field_dict["modified"] = modified

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        offering_name = d.pop("offering__name", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        identity_name = d.pop("identity__name", UNSET)

        state = d.pop("state", UNSET)

        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified, Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)

        cleanup_response_item = cls(
            uuid=uuid,
            name=name,
            offering_name=offering_name,
            created=created,
            identity_name=identity_name,
            state=state,
            modified=modified,
        )

        cleanup_response_item.additional_properties = d
        return cleanup_response_item

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
