from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.bulk_upsert_permission_overrides_dto_overrides_item import BulkUpsertPermissionOverridesDtoOverridesItem





T = TypeVar("T", bound="BulkUpsertPermissionOverridesDto")



@_attrs_define
class BulkUpsertPermissionOverridesDto:
    """ Request payload for bulk-upserting permission overrides on an environment.

        Attributes:
            overrides (list[BulkUpsertPermissionOverridesDtoOverridesItem]): List of override rows to upsert; each
                (userEmail, permission, field) combination must be unique within the array.
     """

    overrides: list[BulkUpsertPermissionOverridesDtoOverridesItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.bulk_upsert_permission_overrides_dto_overrides_item import BulkUpsertPermissionOverridesDtoOverridesItem # noqa: PLC0415
        overrides = []
        for overrides_item_data in self.overrides:
            overrides_item = overrides_item_data.to_dict()
            overrides.append(overrides_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "overrides": overrides,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bulk_upsert_permission_overrides_dto_overrides_item import BulkUpsertPermissionOverridesDtoOverridesItem # noqa: PLC0415
        d = dict(src_dict)
        overrides = []
        _overrides = d.pop("overrides")
        for overrides_item_data in (_overrides):
            overrides_item = BulkUpsertPermissionOverridesDtoOverridesItem.from_dict(overrides_item_data)



            overrides.append(overrides_item)


        bulk_upsert_permission_overrides_dto = cls(
            overrides=overrides,
        )


        bulk_upsert_permission_overrides_dto.additional_properties = d
        return bulk_upsert_permission_overrides_dto

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
