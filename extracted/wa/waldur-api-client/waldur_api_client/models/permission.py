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
        uuid (Union[Unset, UUID]):
        user_uuid (Union[Unset, UUID]):
        user_name (Union[Unset, str]):
        user_slug (Union[Unset, str]):
        user_username (Union[Unset, str]):
        user_email (Union[Unset, str]):
        created (Union[Unset, datetime.datetime]):
        expiration_time (Union[None, Unset, datetime.datetime]):
        is_active (Union[None, Unset, bool]):
        created_by_full_name (Union[Unset, str]):
        created_by_username (Union[Unset, str]):
        revoked_by_full_name (Union[None, Unset, str]):
        revoked_by_username (Union[None, Unset, str]):
        revoke_reason (Union[Unset, str]):
        role_name (Union[Unset, str]):
        role_description (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope_type (Union[None, Unset, str]):
        scope_uuid (Union[Unset, UUID]):
        scope_name (Union[Unset, str]):
        scope_is_removed (Union[Unset, bool]):
        customer_uuid (Union[Unset, UUID]):
        customer_name (Union[Unset, str]):
        resource_uuid (Union[None, UUID, Unset]):
        project_uuid (Union[None, UUID, Unset]):
    """

    uuid: Union[Unset, UUID] = UNSET
    user_uuid: Union[Unset, UUID] = UNSET
    user_name: Union[Unset, str] = UNSET
    user_slug: Union[Unset, str] = UNSET
    user_username: Union[Unset, str] = UNSET
    user_email: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    expiration_time: Union[None, Unset, datetime.datetime] = UNSET
    is_active: Union[None, Unset, bool] = UNSET
    created_by_full_name: Union[Unset, str] = UNSET
    created_by_username: Union[Unset, str] = UNSET
    revoked_by_full_name: Union[None, Unset, str] = UNSET
    revoked_by_username: Union[None, Unset, str] = UNSET
    revoke_reason: Union[Unset, str] = UNSET
    role_name: Union[Unset, str] = UNSET
    role_description: Union[Unset, str] = UNSET
    role_uuid: Union[Unset, UUID] = UNSET
    scope_type: Union[None, Unset, str] = UNSET
    scope_uuid: Union[Unset, UUID] = UNSET
    scope_name: Union[Unset, str] = UNSET
    scope_is_removed: Union[Unset, bool] = UNSET
    customer_uuid: Union[Unset, UUID] = UNSET
    customer_name: Union[Unset, str] = UNSET
    resource_uuid: Union[None, UUID, Unset] = UNSET
    project_uuid: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        user_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.user_uuid, Unset):
            user_uuid = str(self.user_uuid)

        user_name = self.user_name

        user_slug = self.user_slug

        user_username = self.user_username

        user_email = self.user_email

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

        is_active: Union[None, Unset, bool]
        if isinstance(self.is_active, Unset):
            is_active = UNSET
        else:
            is_active = self.is_active

        created_by_full_name = self.created_by_full_name

        created_by_username = self.created_by_username

        revoked_by_full_name: Union[None, Unset, str]
        if isinstance(self.revoked_by_full_name, Unset):
            revoked_by_full_name = UNSET
        else:
            revoked_by_full_name = self.revoked_by_full_name

        revoked_by_username: Union[None, Unset, str]
        if isinstance(self.revoked_by_username, Unset):
            revoked_by_username = UNSET
        else:
            revoked_by_username = self.revoked_by_username

        revoke_reason = self.revoke_reason

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

        scope_is_removed = self.scope_is_removed

        customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.customer_uuid, Unset):
            customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        resource_uuid: Union[None, Unset, str]
        if isinstance(self.resource_uuid, Unset):
            resource_uuid = UNSET
        elif isinstance(self.resource_uuid, UUID):
            resource_uuid = str(self.resource_uuid)
        else:
            resource_uuid = self.resource_uuid

        project_uuid: Union[None, Unset, str]
        if isinstance(self.project_uuid, Unset):
            project_uuid = UNSET
        elif isinstance(self.project_uuid, UUID):
            project_uuid = str(self.project_uuid)
        else:
            project_uuid = self.project_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if user_uuid is not UNSET:
            field_dict["user_uuid"] = user_uuid
        if user_name is not UNSET:
            field_dict["user_name"] = user_name
        if user_slug is not UNSET:
            field_dict["user_slug"] = user_slug
        if user_username is not UNSET:
            field_dict["user_username"] = user_username
        if user_email is not UNSET:
            field_dict["user_email"] = user_email
        if created is not UNSET:
            field_dict["created"] = created
        if expiration_time is not UNSET:
            field_dict["expiration_time"] = expiration_time
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if created_by_full_name is not UNSET:
            field_dict["created_by_full_name"] = created_by_full_name
        if created_by_username is not UNSET:
            field_dict["created_by_username"] = created_by_username
        if revoked_by_full_name is not UNSET:
            field_dict["revoked_by_full_name"] = revoked_by_full_name
        if revoked_by_username is not UNSET:
            field_dict["revoked_by_username"] = revoked_by_username
        if revoke_reason is not UNSET:
            field_dict["revoke_reason"] = revoke_reason
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
        if scope_is_removed is not UNSET:
            field_dict["scope_is_removed"] = scope_is_removed
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name
        if resource_uuid is not UNSET:
            field_dict["resource_uuid"] = resource_uuid
        if project_uuid is not UNSET:
            field_dict["project_uuid"] = project_uuid

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

        _user_uuid = d.pop("user_uuid", UNSET)
        user_uuid: Union[Unset, UUID]
        if isinstance(_user_uuid, Unset):
            user_uuid = UNSET
        else:
            user_uuid = UUID(_user_uuid)

        user_name = d.pop("user_name", UNSET)

        user_slug = d.pop("user_slug", UNSET)

        user_username = d.pop("user_username", UNSET)

        user_email = d.pop("user_email", UNSET)

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

        def _parse_is_active(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_active = _parse_is_active(d.pop("is_active", UNSET))

        created_by_full_name = d.pop("created_by_full_name", UNSET)

        created_by_username = d.pop("created_by_username", UNSET)

        def _parse_revoked_by_full_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        revoked_by_full_name = _parse_revoked_by_full_name(d.pop("revoked_by_full_name", UNSET))

        def _parse_revoked_by_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        revoked_by_username = _parse_revoked_by_username(d.pop("revoked_by_username", UNSET))

        revoke_reason = d.pop("revoke_reason", UNSET)

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

        scope_is_removed = d.pop("scope_is_removed", UNSET)

        _customer_uuid = d.pop("customer_uuid", UNSET)
        customer_uuid: Union[Unset, UUID]
        if isinstance(_customer_uuid, Unset):
            customer_uuid = UNSET
        else:
            customer_uuid = UUID(_customer_uuid)

        customer_name = d.pop("customer_name", UNSET)

        def _parse_resource_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resource_uuid_type_0 = UUID(data)

                return resource_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        resource_uuid = _parse_resource_uuid(d.pop("resource_uuid", UNSET))

        def _parse_project_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_uuid_type_0 = UUID(data)

                return project_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        project_uuid = _parse_project_uuid(d.pop("project_uuid", UNSET))

        permission = cls(
            uuid=uuid,
            user_uuid=user_uuid,
            user_name=user_name,
            user_slug=user_slug,
            user_username=user_username,
            user_email=user_email,
            created=created,
            expiration_time=expiration_time,
            is_active=is_active,
            created_by_full_name=created_by_full_name,
            created_by_username=created_by_username,
            revoked_by_full_name=revoked_by_full_name,
            revoked_by_username=revoked_by_username,
            revoke_reason=revoke_reason,
            role_name=role_name,
            role_description=role_description,
            role_uuid=role_uuid,
            scope_type=scope_type,
            scope_uuid=scope_uuid,
            scope_name=scope_name,
            scope_is_removed=scope_is_removed,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            resource_uuid=resource_uuid,
            project_uuid=project_uuid,
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
