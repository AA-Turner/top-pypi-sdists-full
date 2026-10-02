from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.bulk_soft_delete_body_dto_filter_mode import BulkSoftDeleteBodyDtoFilterMode
from typing import cast

if TYPE_CHECKING:
  from ..models.bulk_soft_delete_body_dto_filter_filter import BulkSoftDeleteBodyDtoFilterFilter





T = TypeVar("T", bound="BulkSoftDeleteBodyDtoFilter")



@_attrs_define
class BulkSoftDeleteBodyDtoFilter:
    """ 
        Attributes:
            mode (BulkSoftDeleteBodyDtoFilterMode): Caller is supplying a problem-list filter; the server resolves matching
                problems and soft-deletes them.
            filter_ (BulkSoftDeleteBodyDtoFilterFilter): Filter describing which problems to soft-delete, resolved server-
                side.
     """

    mode: BulkSoftDeleteBodyDtoFilterMode
    filter_: BulkSoftDeleteBodyDtoFilterFilter
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.bulk_soft_delete_body_dto_filter_filter import BulkSoftDeleteBodyDtoFilterFilter # noqa: PLC0415
        mode = self.mode.value

        filter_ = self.filter_.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "mode": mode,
            "filter": filter_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bulk_soft_delete_body_dto_filter_filter import BulkSoftDeleteBodyDtoFilterFilter # noqa: PLC0415
        d = dict(src_dict)
        mode = BulkSoftDeleteBodyDtoFilterMode(d.pop("mode"))




        filter_ = BulkSoftDeleteBodyDtoFilterFilter.from_dict(d.pop("filter"))




        bulk_soft_delete_body_dto_filter = cls(
            mode=mode,
            filter_=filter_,
        )


        bulk_soft_delete_body_dto_filter.additional_properties = d
        return bulk_soft_delete_body_dto_filter

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
