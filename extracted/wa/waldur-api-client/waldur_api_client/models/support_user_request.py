from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SupportUserRequest")


@_attrs_define
class SupportUserRequest:
    """
    Attributes:
        name (str):
        backend_id (Union[None, Unset, str]):
        backend_name (Union[None, Unset, str]):
        is_active (Union[Unset, bool]): Designates whether this user should be treated as active. Unselect this instead
            of deleting accounts.
        user (Union[None, Unset, str]):
    """

    name: str
    backend_id: Union[None, Unset, str] = UNSET
    backend_name: Union[None, Unset, str] = UNSET
    is_active: Union[Unset, bool] = UNSET
    user: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        backend_id: Union[None, Unset, str]
        if isinstance(self.backend_id, Unset):
            backend_id = UNSET
        else:
            backend_id = self.backend_id

        backend_name: Union[None, Unset, str]
        if isinstance(self.backend_name, Unset):
            backend_name = UNSET
        else:
            backend_name = self.backend_name

        is_active = self.is_active

        user: Union[None, Unset, str]
        if isinstance(self.user, Unset):
            user = UNSET
        else:
            user = self.user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if backend_name is not UNSET:
            field_dict["backend_name"] = backend_name
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_backend_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        backend_id = _parse_backend_id(d.pop("backend_id", UNSET))

        def _parse_backend_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        backend_name = _parse_backend_name(d.pop("backend_name", UNSET))

        is_active = d.pop("is_active", UNSET)

        def _parse_user(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user = _parse_user(d.pop("user", UNSET))

        support_user_request = cls(
            name=name,
            backend_id=backend_id,
            backend_name=backend_name,
            is_active=is_active,
            user=user,
        )

        support_user_request.additional_properties = d
        return support_user_request

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
