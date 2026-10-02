import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectPermissionLog")


@_attrs_define
class ProjectPermissionLog:
    """
    Attributes:
        created (Union[Unset, datetime.datetime]):
        expiration_time (Union[None, Unset, datetime.datetime]):
        created_by (Union[None, Unset, str]):
        created_by_full_name (Union[None, Unset, str]):
        created_by_username (Union[None, Unset, str]): Required. 128 characters or fewer. Lowercase letters, numbers and
            @/./+/-/_ characters
        project (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_created (Union[Unset, datetime.datetime]):
        project_end_date (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        customer_name (Union[Unset, str]):
        role (Union[Unset, str]):
        role_name (Union[Unset, str]):
        user (Union[Unset, str]):
        user_full_name (Union[Unset, str]):
        user_native_name (Union[Unset, str]):
        user_username (Union[Unset, str]): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_
            characters
        user_uuid (Union[Unset, UUID]):
        user_email (Union[Unset, str]):
    """

    created: Union[Unset, datetime.datetime] = UNSET
    expiration_time: Union[None, Unset, datetime.datetime] = UNSET
    created_by: Union[None, Unset, str] = UNSET
    created_by_full_name: Union[None, Unset, str] = UNSET
    created_by_username: Union[None, Unset, str] = UNSET
    project: Union[Unset, str] = UNSET
    project_uuid: Union[Unset, UUID] = UNSET
    project_name: Union[Unset, str] = UNSET
    project_created: Union[Unset, datetime.datetime] = UNSET
    project_end_date: Union[Unset, datetime.datetime] = UNSET
    customer_uuid: Union[Unset, UUID] = UNSET
    customer_name: Union[Unset, str] = UNSET
    role: Union[Unset, str] = UNSET
    role_name: Union[Unset, str] = UNSET
    user: Union[Unset, str] = UNSET
    user_full_name: Union[Unset, str] = UNSET
    user_native_name: Union[Unset, str] = UNSET
    user_username: Union[Unset, str] = UNSET
    user_uuid: Union[Unset, UUID] = UNSET
    user_email: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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

        created_by: Union[None, Unset, str]
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        created_by_full_name: Union[None, Unset, str]
        if isinstance(self.created_by_full_name, Unset):
            created_by_full_name = UNSET
        else:
            created_by_full_name = self.created_by_full_name

        created_by_username: Union[None, Unset, str]
        if isinstance(self.created_by_username, Unset):
            created_by_username = UNSET
        else:
            created_by_username = self.created_by_username

        project = self.project

        project_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.project_uuid, Unset):
            project_uuid = str(self.project_uuid)

        project_name = self.project_name

        project_created: Union[Unset, str] = UNSET
        if not isinstance(self.project_created, Unset):
            project_created = self.project_created.isoformat()

        project_end_date: Union[Unset, str] = UNSET
        if not isinstance(self.project_end_date, Unset):
            project_end_date = self.project_end_date.isoformat()

        customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.customer_uuid, Unset):
            customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        role = self.role

        role_name = self.role_name

        user = self.user

        user_full_name = self.user_full_name

        user_native_name = self.user_native_name

        user_username = self.user_username

        user_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.user_uuid, Unset):
            user_uuid = str(self.user_uuid)

        user_email = self.user_email

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created is not UNSET:
            field_dict["created"] = created
        if expiration_time is not UNSET:
            field_dict["expiration_time"] = expiration_time
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if created_by_full_name is not UNSET:
            field_dict["created_by_full_name"] = created_by_full_name
        if created_by_username is not UNSET:
            field_dict["created_by_username"] = created_by_username
        if project is not UNSET:
            field_dict["project"] = project
        if project_uuid is not UNSET:
            field_dict["project_uuid"] = project_uuid
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if project_created is not UNSET:
            field_dict["project_created"] = project_created
        if project_end_date is not UNSET:
            field_dict["project_end_date"] = project_end_date
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name
        if role is not UNSET:
            field_dict["role"] = role
        if role_name is not UNSET:
            field_dict["role_name"] = role_name
        if user is not UNSET:
            field_dict["user"] = user
        if user_full_name is not UNSET:
            field_dict["user_full_name"] = user_full_name
        if user_native_name is not UNSET:
            field_dict["user_native_name"] = user_native_name
        if user_username is not UNSET:
            field_dict["user_username"] = user_username
        if user_uuid is not UNSET:
            field_dict["user_uuid"] = user_uuid
        if user_email is not UNSET:
            field_dict["user_email"] = user_email

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
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

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_created_by_full_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by_full_name = _parse_created_by_full_name(d.pop("created_by_full_name", UNSET))

        def _parse_created_by_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by_username = _parse_created_by_username(d.pop("created_by_username", UNSET))

        project = d.pop("project", UNSET)

        _project_uuid = d.pop("project_uuid", UNSET)
        project_uuid: Union[Unset, UUID]
        if isinstance(_project_uuid, Unset):
            project_uuid = UNSET
        else:
            project_uuid = UUID(_project_uuid)

        project_name = d.pop("project_name", UNSET)

        _project_created = d.pop("project_created", UNSET)
        project_created: Union[Unset, datetime.datetime]
        if isinstance(_project_created, Unset):
            project_created = UNSET
        else:
            project_created = isoparse(_project_created)

        _project_end_date = d.pop("project_end_date", UNSET)
        project_end_date: Union[Unset, datetime.datetime]
        if isinstance(_project_end_date, Unset):
            project_end_date = UNSET
        else:
            project_end_date = isoparse(_project_end_date)

        _customer_uuid = d.pop("customer_uuid", UNSET)
        customer_uuid: Union[Unset, UUID]
        if isinstance(_customer_uuid, Unset):
            customer_uuid = UNSET
        else:
            customer_uuid = UUID(_customer_uuid)

        customer_name = d.pop("customer_name", UNSET)

        role = d.pop("role", UNSET)

        role_name = d.pop("role_name", UNSET)

        user = d.pop("user", UNSET)

        user_full_name = d.pop("user_full_name", UNSET)

        user_native_name = d.pop("user_native_name", UNSET)

        user_username = d.pop("user_username", UNSET)

        _user_uuid = d.pop("user_uuid", UNSET)
        user_uuid: Union[Unset, UUID]
        if isinstance(_user_uuid, Unset):
            user_uuid = UNSET
        else:
            user_uuid = UUID(_user_uuid)

        user_email = d.pop("user_email", UNSET)

        project_permission_log = cls(
            created=created,
            expiration_time=expiration_time,
            created_by=created_by,
            created_by_full_name=created_by_full_name,
            created_by_username=created_by_username,
            project=project,
            project_uuid=project_uuid,
            project_name=project_name,
            project_created=project_created,
            project_end_date=project_end_date,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            role=role,
            role_name=role_name,
            user=user,
            user_full_name=user_full_name,
            user_native_name=user_native_name,
            user_username=user_username,
            user_uuid=user_uuid,
            user_email=user_email,
        )

        project_permission_log.additional_properties = d
        return project_permission_log

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
