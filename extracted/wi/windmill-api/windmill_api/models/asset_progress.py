from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.asset_progress_asset_kind import AssetProgressAssetKind
from ..models.asset_progress_status import AssetProgressStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssetProgress")


@_attrs_define
class AssetProgress:
    """
    Attributes:
        asset_kind (AssetProgressAssetKind):
        asset_path (str):
        status (AssetProgressStatus):
        row_count (Union[Unset, None, int]):
        error (Union[Unset, None, str]):
    """

    asset_kind: AssetProgressAssetKind
    asset_path: str
    status: AssetProgressStatus
    row_count: Union[Unset, None, int] = UNSET
    error: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        asset_kind = self.asset_kind.value

        asset_path = self.asset_path
        status = self.status.value

        row_count = self.row_count
        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "asset_kind": asset_kind,
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
        asset_kind = AssetProgressAssetKind(d.pop("asset_kind"))

        asset_path = d.pop("asset_path")

        status = AssetProgressStatus(d.pop("status"))

        row_count = d.pop("row_count", UNSET)

        error = d.pop("error", UNSET)

        asset_progress = cls(
            asset_kind=asset_kind,
            asset_path=asset_path,
            status=status,
            row_count=row_count,
            error=error,
        )

        asset_progress.additional_properties = d
        return asset_progress

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
