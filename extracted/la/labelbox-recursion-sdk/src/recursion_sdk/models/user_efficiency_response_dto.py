from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.user_efficiency_response_dto_rows_item import UserEfficiencyResponseDtoRowsItem





T = TypeVar("T", bound="UserEfficiencyResponseDto")



@_attrs_define
class UserEfficiencyResponseDto:
    """ Response payload for the user-efficiency report.

        Attributes:
            rows (list[UserEfficiencyResponseDtoRowsItem]): One efficiency row per user included in the report.
     """

    rows: list[UserEfficiencyResponseDtoRowsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.user_efficiency_response_dto_rows_item import UserEfficiencyResponseDtoRowsItem # noqa: PLC0415
        rows = []
        for rows_item_data in self.rows:
            rows_item = rows_item_data.to_dict()
            rows.append(rows_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "rows": rows,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_efficiency_response_dto_rows_item import UserEfficiencyResponseDtoRowsItem # noqa: PLC0415
        d = dict(src_dict)
        rows = []
        _rows = d.pop("rows")
        for rows_item_data in (_rows):
            rows_item = UserEfficiencyResponseDtoRowsItem.from_dict(rows_item_data)



            rows.append(rows_item)


        user_efficiency_response_dto = cls(
            rows=rows,
        )

        return user_efficiency_response_dto

