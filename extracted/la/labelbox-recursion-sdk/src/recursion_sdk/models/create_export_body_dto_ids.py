from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_export_body_dto_ids_format import CreateExportBodyDtoIdsFormat
from ..models.create_export_body_dto_ids_mode import CreateExportBodyDtoIdsMode
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="CreateExportBodyDtoIds")



@_attrs_define
class CreateExportBodyDtoIds:
    """ 
        Attributes:
            mode (CreateExportBodyDtoIdsMode): Caller is supplying an explicit list of problem IDs to export.
            problem_ids (list[UUID]): Explicit list of problem IDs to include in the archive, capped at the worker hard
                problem limit.
            format_ (CreateExportBodyDtoIdsFormat | Unset): Archive format for the export. Defaults to the standard layout
                when omitted.
     """

    mode: CreateExportBodyDtoIdsMode
    problem_ids: list[UUID]
    format_: CreateExportBodyDtoIdsFormat | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        mode = self.mode.value

        problem_ids = []
        for problem_ids_item_data in self.problem_ids:
            problem_ids_item = str(problem_ids_item_data)
            problem_ids.append(problem_ids_item)



        format_: str | Unset = UNSET
        if not isinstance(self.format_, Unset):
            format_ = self.format_.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "mode": mode,
            "problemIds": problem_ids,
        })
        if format_ is not UNSET:
            field_dict["format"] = format_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = CreateExportBodyDtoIdsMode(d.pop("mode"))




        problem_ids = []
        _problem_ids = d.pop("problemIds")
        for problem_ids_item_data in (_problem_ids):
            problem_ids_item = UUID(problem_ids_item_data)



            problem_ids.append(problem_ids_item)


        _format_ = d.pop("format", UNSET)
        format_: CreateExportBodyDtoIdsFormat | Unset
        if isinstance(_format_,  Unset):
            format_ = UNSET
        else:
            format_ = CreateExportBodyDtoIdsFormat(_format_)




        create_export_body_dto_ids = cls(
            mode=mode,
            problem_ids=problem_ids,
            format_=format_,
        )


        create_export_body_dto_ids.additional_properties = d
        return create_export_body_dto_ids

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
