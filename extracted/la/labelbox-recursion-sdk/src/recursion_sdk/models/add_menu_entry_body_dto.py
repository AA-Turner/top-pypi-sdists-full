from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="AddMenuEntryBodyDto")



@_attrs_define
class AddMenuEntryBodyDto:
    """ Request body for adding one run-config version to a slot menu.

        Example:
            {'runConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad', 'isDefault': True}

        Attributes:
            run_config_version_id (UUID): Locked, slot-reachable run-config version to add to the menu.
            is_default (bool | Unset): When true, star this entry (include it in the slot default set).
     """

    run_config_version_id: UUID
    is_default: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        run_config_version_id = str(self.run_config_version_id)

        is_default = self.is_default


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "runConfigVersionId": run_config_version_id,
        })
        if is_default is not UNSET:
            field_dict["isDefault"] = is_default

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        run_config_version_id = UUID(d.pop("runConfigVersionId"))




        is_default = d.pop("isDefault", UNSET)

        add_menu_entry_body_dto = cls(
            run_config_version_id=run_config_version_id,
            is_default=is_default,
        )


        add_menu_entry_body_dto.additional_properties = d
        return add_menu_entry_body_dto

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
