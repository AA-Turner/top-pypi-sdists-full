from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RecordDbtRunProgressJsonBodyItem")


@_attrs_define
class RecordDbtRunProgressJsonBodyItem:
    """
    Attributes:
        asset_path (str):
        status (str):
        row_count (Union[Unset, int]):
        error (Union[Unset, str]):
    """

    asset_path: str
    status: str
    row_count: Union[Unset, int] = UNSET
    error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        asset_path = self.asset_path
        status = self.status
        row_count = self.row_count
        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "asset_path": asset_path,
                "status": status,
            }
        )
        if row_count is not UNSET:
            field_dict["row_count"] = row_count
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        asset_path = d.pop("asset_path")

        status = d.pop("status")

        row_count = d.pop("row_count", UNSET)

        error = d.pop("error", UNSET)

        record_dbt_run_progress_json_body_item = cls(
            asset_path=asset_path,
            status=status,
            row_count=row_count,
            error=error,
        )

        record_dbt_run_progress_json_body_item.additional_properties = d
        return record_dbt_run_progress_json_body_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
