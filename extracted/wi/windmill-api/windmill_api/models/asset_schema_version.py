import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_schema_version_columns_item import AssetSchemaVersionColumnsItem


T = TypeVar("T", bound="AssetSchemaVersion")


@_attrs_define
class AssetSchemaVersion:
    """
    Attributes:
        version (int):
        columns (List['AssetSchemaVersionColumnsItem']):
        captured_at (datetime.datetime):
        snapshot_id (Union[Unset, None, int]):
        job_id (Union[Unset, None, str]):
    """

    version: int
    columns: List["AssetSchemaVersionColumnsItem"]
    captured_at: datetime.datetime
    snapshot_id: Union[Unset, None, int] = UNSET
    job_id: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        version = self.version
        columns = []
        for columns_item_data in self.columns:
            columns_item = columns_item_data.to_dict()

            columns.append(columns_item)

        captured_at = self.captured_at.isoformat()

        snapshot_id = self.snapshot_id
        job_id = self.job_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "version": version,
                "columns": columns,
                "captured_at": captured_at,
            }
        )
        if snapshot_id is not UNSET:
            field_dict["snapshot_id"] = snapshot_id
        if job_id is not UNSET:
            field_dict["job_id"] = job_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.asset_schema_version_columns_item import AssetSchemaVersionColumnsItem

        d = src_dict.copy()
        version = d.pop("version")

        columns = []
        _columns = d.pop("columns")
        for columns_item_data in _columns:
            columns_item = AssetSchemaVersionColumnsItem.from_dict(columns_item_data)

            columns.append(columns_item)

        captured_at = isoparse(d.pop("captured_at"))

        snapshot_id = d.pop("snapshot_id", UNSET)

        job_id = d.pop("job_id", UNSET)

        asset_schema_version = cls(
            version=version,
            columns=columns,
            captured_at=captured_at,
            snapshot_id=snapshot_id,
            job_id=job_id,
        )

        asset_schema_version.additional_properties = d
        return asset_schema_version

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
