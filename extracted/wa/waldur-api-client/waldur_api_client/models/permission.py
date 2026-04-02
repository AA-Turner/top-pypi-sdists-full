import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Permission")


@_attrs_define
class Permission:
    """
    Attributes:
        user_uuid (Union[Unset, UUID]):
        user_name (Union[Unset, str]):
        user_slug (Union[Unset, str]):
        created (Union[Unset, datetime.datetime]):
        expiration_time (Union[None, Unset, datetime.datetime]):
        created_by_full_name (Union[Unset, str]):
        created_by_username (Union[Unset, str]):
        role_name (Union[Unset, str]):
        role_description (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope_type (Union[None, Unset, str]):
        scope_uuid (Union[Unset, UUID]):
        scope_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        customer_name (Union[Unset, str]):
    """

    user_uuid: Union[Unset, UUID] = UNSET
    user_name: Union[Unset, str] = UNSET
    user_slug: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    expiration_time: Union[None, Unset, datetime.datetime] = UNSET
    created_by_full_name: Union[Unset, str] = UNSET
    created_by_username: Union[Unset, str] = UNSET
    role_name: Union[Unset, str] = UNSET
    role_description: Union[Unset, str] = UNSET
    role_uuid: Union[Unset, UUID] = UNSET
    scope_type: Union[None, Unset, str] = UNSET
    scope_uuid: Union[Unset, UUID] = UNSET
    scope_name: Union[Unset, str] = UNSET
    customer_uuid: Union[Unset, UUID] = UNSET
    customer_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.user_uuid, Unset):
            user_uuid = str(self.user_uuid)

        user_name = self.user_name

        user_slug = self.user_slug

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        expiration_time: Union[None, Unset, str]
        if isinstance(self.expiration_time, Unset):
            expiration_time = UNSET
        elif isinstance(self.expiration_time, datetime.datetime):
            expiration_time = self.expiration_time.isoformat()
        else:
            expiration_time = self.expiration_time

        created_by_full_name = self.created_by_full_name

        created_by_username = self.created_by_username

        role_name = self.role_name

        role_description = self.role_description

        role_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.role_uuid, Unset):
            role_uuid = str(self.role_uuid)

        scope_type: Union[None, Unset, str]
        if isinstance(self.scope_type, Unset):
            scope_type = UNSET
        else:
            scope_type = self.scope_type

        scope_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.scope_uuid, Unset):
            scope_uuid = str(self.scope_uuid)

        scope_name = self.scope_name

        customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.customer_uuid, Unset):
            customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user_uuid is not UNSET:
            field_dict["user_uuid"] = user_uuid
        if user_name is not UNSET:
            field_dict["user_name"] = user_name
        if user_slug is not UNSET:
            field_dict["user_slug"] = user_slug
        if created is not UNSET:
            field_dict["created"] = created
        if expiration_time is not UNSET:
            field_dict["expiration_time"] = expiration_time
        if created_by_full_name is not UNSET:
            field_dict["created_by_full_name"] = created_by_full_name
        if created_by_username is not UNSET:
            field_dict["created_by_username"] = created_by_username
        if role_name is not UNSET:
            field_dict["role_name"] = role_name
        if role_description is not UNSET:
            field_dict["role_description"] = role_description
        if role_uuid is not UNSET:
            field_dict["role_uuid"] = role_uuid
        if scope_type is not UNSET:
            field_dict["scope_type"] = scope_type
        if scope_uuid is not UNSET:
            field_dict["scope_uuid"] = scope_uuid
        if scope_name is not UNSET:
            field_dict["scope_name"] = scope_name
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _user_uuid = d.pop("user_uuid", UNSET)
        user_uuid: Union[Unset, UUID]
        if isinstance(_user_uuid, Unset):
            user_uuid = UNSET
        else:
            user_uuid = UUID(_user_uuid)

        user_name = d.pop("user_name", UNSET)

        user_slug = d.pop("user_slug", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        def _parse_expiration_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expiration_time_type_0 = isoparse(data)

                return expiration_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        expiration_time = _parse_expiration_time(d.pop("expiration_time", UNSET))

        created_by_full_name = d.pop("created_by_full_name", UNSET)

        created_by_username = d.pop("created_by_username", UNSET)

        role_name = d.pop("role_name", UNSET)

        role_description = d.pop("role_description", UNSET)

        _role_uuid = d.pop("role_uuid", UNSET)
        role_uuid: Union[Unset, UUID]
        if isinstance(_role_uuid, Unset):
            role_uuid = UNSET
        else:
            role_uuid = UUID(_role_uuid)

        def _parse_scope_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        scope_type = _parse_scope_type(d.pop("scope_type", UNSET))

        _scope_uuid = d.pop("scope_uuid", UNSET)
        scope_uuid: Union[Unset, UUID]
        if isinstance(_scope_uuid, Unset):
            scope_uuid = UNSET
        else:
            scope_uuid = UUID(_scope_uuid)

        scope_name = d.pop("scope_name", UNSET)

        _customer_uuid = d.pop("customer_uuid", UNSET)
        customer_uuid: Union[Unset, UUID]
        if isinstance(_customer_uuid, Unset):
            customer_uuid = UNSET
        else:
            customer_uuid = UUID(_customer_uuid)

        customer_name = d.pop("customer_name", UNSET)

        permission = cls(
            user_uuid=user_uuid,
            user_name=user_name,
            user_slug=user_slug,
            created=created,
            expiration_time=expiration_time,
            created_by_full_name=created_by_full_name,
            created_by_username=created_by_username,
            role_name=role_name,
            role_description=role_description,
            role_uuid=role_uuid,
            scope_type=scope_type,
            scope_uuid=scope_uuid,
            scope_name=scope_name,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
        )

        permission.additional_properties = d
        return permission

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
