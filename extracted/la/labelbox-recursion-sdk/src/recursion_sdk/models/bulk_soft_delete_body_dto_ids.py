from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.bulk_soft_delete_body_dto_ids_mode import BulkSoftDeleteBodyDtoIdsMode
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="BulkSoftDeleteBodyDtoIds")



@_attrs_define
class BulkSoftDeleteBodyDtoIds:
    """ 
        Attributes:
            mode (BulkSoftDeleteBodyDtoIdsMode): Caller is supplying an explicit list of problem IDs to soft-delete.
            problem_ids (list[UUID]): Explicit list of problem IDs to soft-delete.
     """

    mode: BulkSoftDeleteBodyDtoIdsMode
    problem_ids: list[UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        mode = self.mode.value

        problem_ids = []
        for problem_ids_item_data in self.problem_ids:
            problem_ids_item = str(problem_ids_item_data)
            problem_ids.append(problem_ids_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "mode": mode,
            "problemIds": problem_ids,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = BulkSoftDeleteBodyDtoIdsMode(d.pop("mode"))




        problem_ids = []
        _problem_ids = d.pop("problemIds")
        for problem_ids_item_data in (_problem_ids):
            problem_ids_item = UUID(problem_ids_item_data)



            problem_ids.append(problem_ids_item)


        bulk_soft_delete_body_dto_ids = cls(
            mode=mode,
            problem_ids=problem_ids,
        )


        bulk_soft_delete_body_dto_ids.additional_properties = d
        return bulk_soft_delete_body_dto_ids

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
