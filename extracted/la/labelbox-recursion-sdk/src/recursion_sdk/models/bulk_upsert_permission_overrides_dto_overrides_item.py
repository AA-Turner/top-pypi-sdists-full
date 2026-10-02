from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.bulk_upsert_permission_overrides_dto_overrides_item_effect import BulkUpsertPermissionOverridesDtoOverridesItemEffect
from ..models.bulk_upsert_permission_overrides_dto_overrides_item_field_type_0_type_0 import BulkUpsertPermissionOverridesDtoOverridesItemFieldType0Type0
from ..models.bulk_upsert_permission_overrides_dto_overrides_item_field_type_0_type_1 import BulkUpsertPermissionOverridesDtoOverridesItemFieldType0Type1
from typing import cast






T = TypeVar("T", bound="BulkUpsertPermissionOverridesDtoOverridesItem")



@_attrs_define
class BulkUpsertPermissionOverridesDtoOverridesItem:
    """ Request payload for creating or updating a single permission override row.

        Attributes:
            user_email (None | str): Email of the user the override targets (lower-cased on accept), or null for an
                environment-wide override.
            permission (str): Permission string to override (must be one of the whitelisted overridable permissions).
            field (BulkUpsertPermissionOverridesDtoOverridesItemFieldType0Type0 |
                BulkUpsertPermissionOverridesDtoOverridesItemFieldType0Type1 | None): Specific field to target, or null for a
                whole-permission override.
            effect (BulkUpsertPermissionOverridesDtoOverridesItemEffect): Whether the override grants or revokes the
                permission/field.
     """

    user_email: None | str
    permission: str
    field: BulkUpsertPermissionOverridesDtoOverridesItemFieldType0Type0 | BulkUpsertPermissionOverridesDtoOverridesItemFieldType0Type1 | None
    effect: BulkUpsertPermissionOverridesDtoOverridesItemEffect
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        user_email: None | str
        user_email = self.user_email

        permission = self.permission

        field: None | str
        if isinstance(self.field, BulkUpsertPermissionOverridesDtoOverridesItemFieldType0Type0):
            field = self.field.value
        elif isinstance(self.field, BulkUpsertPermissionOverridesDtoOverridesItemFieldType0Type1):
            field = self.field.value
        else:
            field = self.field

        effect = self.effect.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "userEmail": user_email,
            "permission": permission,
            "field": field,
            "effect": effect,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_user_email(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        user_email = _parse_user_email(d.pop("userEmail"))


        permission = d.pop("permission")

        def _parse_field(data: object) -> BulkUpsertPermissionOverridesDtoOverridesItemFieldType0Type0 | BulkUpsertPermissionOverridesDtoOverridesItemFieldType0Type1 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                field_type_0_type_0 = BulkUpsertPermissionOverridesDtoOverridesItemFieldType0Type0(data)



                return field_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                field_type_0_type_1 = BulkUpsertPermissionOverridesDtoOverridesItemFieldType0Type1(data)



                return field_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(BulkUpsertPermissionOverridesDtoOverridesItemFieldType0Type0 | BulkUpsertPermissionOverridesDtoOverridesItemFieldType0Type1 | None, data)

        field = _parse_field(d.pop("field"))


        effect = BulkUpsertPermissionOverridesDtoOverridesItemEffect(d.pop("effect"))




        bulk_upsert_permission_overrides_dto_overrides_item = cls(
            user_email=user_email,
            permission=permission,
            field=field,
            effect=effect,
        )


        bulk_upsert_permission_overrides_dto_overrides_item.additional_properties = d
        return bulk_upsert_permission_overrides_dto_overrides_item

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
