import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_asset_partitions_response_200_item_asset_kind import ListAssetPartitionsResponse200ItemAssetKind
from ..models.list_asset_partitions_response_200_item_status import ListAssetPartitionsResponse200ItemStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListAssetPartitionsResponse200Item")


@_attrs_define
class ListAssetPartitionsResponse200Item:
    """
    Attributes:
        asset_kind (ListAssetPartitionsResponse200ItemAssetKind):
        asset_path (str):
        partition (str):
        status (ListAssetPartitionsResponse200ItemStatus):
        materialized_at (datetime.datetime):
        snapshot_id (Union[Unset, None, int]):
        row_count (Union[Unset, None, int]):
        job_id (Union[Unset, None, str]):
        error (Union[Unset, None, str]):
    """

    asset_kind: ListAssetPartitionsResponse200ItemAssetKind
    asset_path: str
    partition: str
    status: ListAssetPartitionsResponse200ItemStatus
    materialized_at: datetime.datetime
    snapshot_id: Union[Unset, None, int] = UNSET
    row_count: Union[Unset, None, int] = UNSET
    job_id: Union[Unset, None, str] = UNSET
    error: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        asset_kind = self.asset_kind.value

        asset_path = self.asset_path
        partition = self.partition
        status = self.status.value

        materialized_at = self.materialized_at.isoformat()

        snapshot_id = self.snapshot_id
        row_count = self.row_count
        job_id = self.job_id
        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "asset_kind": asset_kind,
                "asset_path": asset_path,
                "partition": partition,
                "status": status,
                "materialized_at": materialized_at,
            }
        )
        if snapshot_id is not UNSET:
            field_dict["snapshot_id"] = snapshot_id
        if row_count is not UNSET:
            field_dict["row_count"] = row_count
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        asset_kind = ListAssetPartitionsResponse200ItemAssetKind(d.pop("asset_kind"))

        asset_path = d.pop("asset_path")

        partition = d.pop("partition")

        status = ListAssetPartitionsResponse200ItemStatus(d.pop("status"))

        materialized_at = isoparse(d.pop("materialized_at"))

        snapshot_id = d.pop("snapshot_id", UNSET)

        row_count = d.pop("row_count", UNSET)

        job_id = d.pop("job_id", UNSET)

        error = d.pop("error", UNSET)

        list_asset_partitions_response_200_item = cls(
            asset_kind=asset_kind,
            asset_path=asset_path,
            partition=partition,
            status=status,
            materialized_at=materialized_at,
            snapshot_id=snapshot_id,
            row_count=row_count,
            job_id=job_id,
            error=error,
        )

        list_asset_partitions_response_200_item.additional_properties = d
        return list_asset_partitions_response_200_item

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
