from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="RemoveExternalIdsDto")



@_attrs_define
class RemoveExternalIdsDto:
    """ Request body for bulk-deleting problems in an environment by external ID.

        Example:
            {'externalIds': ['detect-surface-defects', 'classify-weld-quality']}

        Attributes:
            external_ids (list[str]): External identifiers of the problems to soft-delete.
     """

    external_ids: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        external_ids = self.external_ids




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "externalIds": external_ids,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        external_ids = cast(list[str], d.pop("externalIds"))


        remove_external_ids_dto = cls(
            external_ids=external_ids,
        )


        remove_external_ids_dto.additional_properties = d
        return remove_external_ids_dto

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
