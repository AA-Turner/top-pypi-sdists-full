from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SupportUser")


@_attrs_define
class SupportUser:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        backend_id (Union[None, Unset, str]):
        user (Union[None, Unset, str]):
        backend_name (Union[None, Unset, str]):
    """

    url: str
    uuid: UUID
    name: str
    backend_id: Union[None, Unset, str] = UNSET
    user: Union[None, Unset, str] = UNSET
    backend_name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        backend_id: Union[None, Unset, str]
        if isinstance(self.backend_id, Unset):
            backend_id = UNSET
        else:
            backend_id = self.backend_id

        user: Union[None, Unset, str]
        if isinstance(self.user, Unset):
            user = UNSET
        else:
            user = self.user

        backend_name: Union[None, Unset, str]
        if isinstance(self.backend_name, Unset):
            backend_name = UNSET
        else:
            backend_name = self.backend_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
            }
        )
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if user is not UNSET:
            field_dict["user"] = user
        if backend_name is not UNSET:
            field_dict["backend_name"] = backend_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        def _parse_backend_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        backend_id = _parse_backend_id(d.pop("backend_id", UNSET))

        def _parse_user(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user = _parse_user(d.pop("user", UNSET))

        def _parse_backend_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        backend_name = _parse_backend_name(d.pop("backend_name", UNSET))

        support_user = cls(
            url=url,
            uuid=uuid,
            name=name,
            backend_id=backend_id,
            user=user,
            backend_name=backend_name,
        )

        support_user.additional_properties = d
        return support_user

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
