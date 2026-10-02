from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_export_body_dto_filter_format import CreateExportBodyDtoFilterFormat
from ..models.create_export_body_dto_filter_mode import CreateExportBodyDtoFilterMode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.create_export_body_dto_filter_filter import CreateExportBodyDtoFilterFilter





T = TypeVar("T", bound="CreateExportBodyDtoFilter")



@_attrs_define
class CreateExportBodyDtoFilter:
    """ 
        Attributes:
            mode (CreateExportBodyDtoFilterMode): Caller is supplying a problem-list filter; the server resolves matching
                problems at job-start.
            filter_ (CreateExportBodyDtoFilterFilter): Filter describing which problems to include, resolved server-side at
                job-start.
            format_ (CreateExportBodyDtoFilterFormat | Unset): Archive format for the export. Defaults to the standard
                layout when omitted.
     """

    mode: CreateExportBodyDtoFilterMode
    filter_: CreateExportBodyDtoFilterFilter
    format_: CreateExportBodyDtoFilterFormat | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_export_body_dto_filter_filter import CreateExportBodyDtoFilterFilter # noqa: PLC0415
        mode = self.mode.value

        filter_ = self.filter_.to_dict()

        format_: str | Unset = UNSET
        if not isinstance(self.format_, Unset):
            format_ = self.format_.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "mode": mode,
            "filter": filter_,
        })
        if format_ is not UNSET:
            field_dict["format"] = format_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_export_body_dto_filter_filter import CreateExportBodyDtoFilterFilter # noqa: PLC0415
        d = dict(src_dict)
        mode = CreateExportBodyDtoFilterMode(d.pop("mode"))




        filter_ = CreateExportBodyDtoFilterFilter.from_dict(d.pop("filter"))




        _format_ = d.pop("format", UNSET)
        format_: CreateExportBodyDtoFilterFormat | Unset
        if isinstance(_format_,  Unset):
            format_ = UNSET
        else:
            format_ = CreateExportBodyDtoFilterFormat(_format_)




        create_export_body_dto_filter = cls(
            mode=mode,
            filter_=filter_,
            format_=format_,
        )


        create_export_body_dto_filter.additional_properties = d
        return create_export_body_dto_filter

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
