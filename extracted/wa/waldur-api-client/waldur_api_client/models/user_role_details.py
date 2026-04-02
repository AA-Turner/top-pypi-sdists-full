import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserRoleDetails")


@_attrs_define
class UserRoleDetails:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        expiration_time (Union[None, Unset, datetime.datetime]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        user_email (Union[Unset, str]):
        user_full_name (Union[Unset, str]):
        user_username (Union[Unset, str]): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_
            characters
        user_uuid (Union[Unset, UUID]):
        user_image (Union[Unset, str]):
        created_by_full_name (Union[Unset, str]):
        created_by_uuid (Union[Unset, UUID]):
    """

    uuid: Union[Unset, UUID] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    expiration_time: Union[None, Unset, datetime.datetime] = UNSET
    role_name: Union[Unset, str] = UNSET
    role_uuid: Union[Unset, UUID] = UNSET
    user_email: Union[Unset, str] = UNSET
    user_full_name: Union[Unset, str] = UNSET
    user_username: Union[Unset, str] = UNSET
    user_uuid: Union[Unset, UUID] = UNSET
    user_image: Union[Unset, str] = UNSET
    created_by_full_name: Union[Unset, str] = UNSET
    created_by_uuid: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

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

        role_name = self.role_name

        role_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.role_uuid, Unset):
            role_uuid = str(self.role_uuid)

        user_email = self.user_email

        user_full_name = self.user_full_name

        user_username = self.user_username

        user_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.user_uuid, Unset):
            user_uuid = str(self.user_uuid)

        user_image = self.user_image

        created_by_full_name = self.created_by_full_name

        created_by_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.created_by_uuid, Unset):
            created_by_uuid = str(self.created_by_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if created is not UNSET:
            field_dict["created"] = created
        if expiration_time is not UNSET:
            field_dict["expiration_time"] = expiration_time
        if role_name is not UNSET:
            field_dict["role_name"] = role_name
        if role_uuid is not UNSET:
            field_dict["role_uuid"] = role_uuid
        if user_email is not UNSET:
            field_dict["user_email"] = user_email
        if user_full_name is not UNSET:
            field_dict["user_full_name"] = user_full_name
        if user_username is not UNSET:
            field_dict["user_username"] = user_username
        if user_uuid is not UNSET:
            field_dict["user_uuid"] = user_uuid
        if user_image is not UNSET:
            field_dict["user_image"] = user_image
        if created_by_full_name is not UNSET:
            field_dict["created_by_full_name"] = created_by_full_name
        if created_by_uuid is not UNSET:
            field_dict["created_by_uuid"] = created_by_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

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

        role_name = d.pop("role_name", UNSET)

        _role_uuid = d.pop("role_uuid", UNSET)
        role_uuid: Union[Unset, UUID]
        if isinstance(_role_uuid, Unset):
            role_uuid = UNSET
        else:
            role_uuid = UUID(_role_uuid)

        user_email = d.pop("user_email", UNSET)

        user_full_name = d.pop("user_full_name", UNSET)

        user_username = d.pop("user_username", UNSET)

        _user_uuid = d.pop("user_uuid", UNSET)
        user_uuid: Union[Unset, UUID]
        if isinstance(_user_uuid, Unset):
            user_uuid = UNSET
        else:
            user_uuid = UUID(_user_uuid)

        user_image = d.pop("user_image", UNSET)

        created_by_full_name = d.pop("created_by_full_name", UNSET)

        _created_by_uuid = d.pop("created_by_uuid", UNSET)
        created_by_uuid: Union[Unset, UUID]
        if isinstance(_created_by_uuid, Unset):
            created_by_uuid = UNSET
        else:
            created_by_uuid = UUID(_created_by_uuid)

        user_role_details = cls(
            uuid=uuid,
            created=created,
            expiration_time=expiration_time,
            role_name=role_name,
            role_uuid=role_uuid,
            user_email=user_email,
            user_full_name=user_full_name,
            user_username=user_username,
            user_uuid=user_uuid,
            user_image=user_image,
            created_by_full_name=created_by_full_name,
            created_by_uuid=created_by_uuid,
        )

        user_role_details.additional_properties = d
        return user_role_details

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
