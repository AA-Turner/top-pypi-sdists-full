from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.permission_override_list_dto_item_effect import PermissionOverrideListDtoItemEffect
from ..models.permission_override_list_dto_item_field_type_0_type_0 import PermissionOverrideListDtoItemFieldType0Type0
from ..models.permission_override_list_dto_item_field_type_0_type_1 import PermissionOverrideListDtoItemFieldType0Type1
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="PermissionOverrideListDtoItem")



@_attrs_define
class PermissionOverrideListDtoItem:
    """ A single environment-scoped permission override; either grants or denies a permission (optionally narrowed to a
    specific field) for a user or for everyone in the environment.

        Attributes:
            id (UUID): Stable permission-override identifier (UUID).
            environment_id (UUID): Environment this override applies within.
            user_email (None | str): Lower-cased email of the user this override targets, or null for an environment-wide
                override applying to all users.
            permission (str): Permission string the override applies to (must be one of the whitelisted overridable
                permissions, e.g. "versions:update").
            field (None | PermissionOverrideListDtoItemFieldType0Type0 | PermissionOverrideListDtoItemFieldType0Type1):
                Specific field name to target, or null for a whole-permission override; required for jobs:create and constrained
                by permission for versions:update.
            effect (PermissionOverrideListDtoItemEffect): Whether the override grants or revokes the permission/field.
            created_at (datetime.datetime): Timestamp when the override was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the override was last updated (ISO-8601, UTC).
     """

    id: UUID
    environment_id: UUID
    user_email: None | str
    permission: str
    field: None | PermissionOverrideListDtoItemFieldType0Type0 | PermissionOverrideListDtoItemFieldType0Type1
    effect: PermissionOverrideListDtoItemEffect
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        environment_id = str(self.environment_id)

        user_email: None | str
        user_email = self.user_email

        permission = self.permission

        field: None | str
        if isinstance(self.field, PermissionOverrideListDtoItemFieldType0Type0):
            field = self.field.value
        elif isinstance(self.field, PermissionOverrideListDtoItemFieldType0Type1):
            field = self.field.value
        else:
            field = self.field

        effect = self.effect.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "environmentId": environment_id,
            "userEmail": user_email,
            "permission": permission,
            "field": field,
            "effect": effect,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        environment_id = UUID(d.pop("environmentId"))




        def _parse_user_email(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        user_email = _parse_user_email(d.pop("userEmail"))


        permission = d.pop("permission")

        def _parse_field(data: object) -> None | PermissionOverrideListDtoItemFieldType0Type0 | PermissionOverrideListDtoItemFieldType0Type1:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                field_type_0_type_0 = PermissionOverrideListDtoItemFieldType0Type0(data)



                return field_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                field_type_0_type_1 = PermissionOverrideListDtoItemFieldType0Type1(data)



                return field_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PermissionOverrideListDtoItemFieldType0Type0 | PermissionOverrideListDtoItemFieldType0Type1, data)

        field = _parse_field(d.pop("field"))


        effect = PermissionOverrideListDtoItemEffect(d.pop("effect"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        permission_override_list_dto_item = cls(
            id=id,
            environment_id=environment_id,
            user_email=user_email,
            permission=permission,
            field=field,
            effect=effect,
            created_at=created_at,
            updated_at=updated_at,
        )

        return permission_override_list_dto_item

