import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingPermission")


@_attrs_define
class OfferingPermission:
    """
    Attributes:
        url (str):
        pk (int):
        created (datetime.datetime):
        created_by (Union[None, str]):
        offering (str):
        offering_uuid (UUID):
        offering_slug (str):
        offering_name (str):
        role (str):
        role_name (str):
        user (str):
        user_full_name (str):
        user_native_name (str):
        user_username (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_ characters
        user_uuid (UUID):
        user_email (str):
        expiration_time (Union[None, Unset, datetime.datetime]):
    """

    url: str
    pk: int
    created: datetime.datetime
    created_by: Union[None, str]
    offering: str
    offering_uuid: UUID
    offering_slug: str
    offering_name: str
    role: str
    role_name: str
    user: str
    user_full_name: str
    user_native_name: str
    user_username: str
    user_uuid: UUID
    user_email: str
    expiration_time: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        pk = self.pk

        created = self.created.isoformat()

        created_by: Union[None, str]
        created_by = self.created_by

        offering = self.offering

        offering_uuid = str(self.offering_uuid)

        offering_slug = self.offering_slug

        offering_name = self.offering_name

        role = self.role

        role_name = self.role_name

        user = self.user

        user_full_name = self.user_full_name

        user_native_name = self.user_native_name

        user_username = self.user_username

        user_uuid = str(self.user_uuid)

        user_email = self.user_email

        expiration_time: Union[None, Unset, str]
        if isinstance(self.expiration_time, Unset):
            expiration_time = UNSET
        elif isinstance(self.expiration_time, datetime.datetime):
            expiration_time = self.expiration_time.isoformat()
        else:
            expiration_time = self.expiration_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "pk": pk,
                "created": created,
                "created_by": created_by,
                "offering": offering,
                "offering_uuid": offering_uuid,
                "offering_slug": offering_slug,
                "offering_name": offering_name,
                "role": role,
                "role_name": role_name,
                "user": user,
                "user_full_name": user_full_name,
                "user_native_name": user_native_name,
                "user_username": user_username,
                "user_uuid": user_uuid,
                "user_email": user_email,
            }
        )
        if expiration_time is not UNSET:
            field_dict["expiration_time"] = expiration_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        pk = d.pop("pk")

        created = isoparse(d.pop("created"))

        def _parse_created_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        created_by = _parse_created_by(d.pop("created_by"))

        offering = d.pop("offering")

        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_slug = d.pop("offering_slug")

        offering_name = d.pop("offering_name")

        role = d.pop("role")

        role_name = d.pop("role_name")

        user = d.pop("user")

        user_full_name = d.pop("user_full_name")

        user_native_name = d.pop("user_native_name")

        user_username = d.pop("user_username")

        user_uuid = UUID(d.pop("user_uuid"))

        user_email = d.pop("user_email")

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

        offering_permission = cls(
            url=url,
            pk=pk,
            created=created,
            created_by=created_by,
            offering=offering,
            offering_uuid=offering_uuid,
            offering_slug=offering_slug,
            offering_name=offering_name,
            role=role,
            role_name=role_name,
            user=user,
            user_full_name=user_full_name,
            user_native_name=user_native_name,
            user_username=user_username,
            user_uuid=user_uuid,
            user_email=user_email,
            expiration_time=expiration_time,
        )

        offering_permission.additional_properties = d
        return offering_permission

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
