from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="QueryPerformance")


@_attrs_define
class QueryPerformance:
    """
    Attributes:
        seq_scan_count (int): Total sequential scans (potentially expensive)
        seq_scan_rows (int): Total rows fetched by sequential scans
        index_scan_count (int): Total index scans
        index_scan_rows (int): Total rows fetched by index scans
        temp_files_count (int): Number of temporary files created
        temp_files_bytes (int): Total size of temporary files in bytes
    """

    seq_scan_count: int
    seq_scan_rows: int
    index_scan_count: int
    index_scan_rows: int
    temp_files_count: int
    temp_files_bytes: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        seq_scan_count = self.seq_scan_count

        seq_scan_rows = self.seq_scan_rows

        index_scan_count = self.index_scan_count

        index_scan_rows = self.index_scan_rows

        temp_files_count = self.temp_files_count

        temp_files_bytes = self.temp_files_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "seq_scan_count": seq_scan_count,
                "seq_scan_rows": seq_scan_rows,
                "index_scan_count": index_scan_count,
                "index_scan_rows": index_scan_rows,
                "temp_files_count": temp_files_count,
                "temp_files_bytes": temp_files_bytes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        seq_scan_count = d.pop("seq_scan_count")

        seq_scan_rows = d.pop("seq_scan_rows")

        index_scan_count = d.pop("index_scan_count")

        index_scan_rows = d.pop("index_scan_rows")

        temp_files_count = d.pop("temp_files_count")

        temp_files_bytes = d.pop("temp_files_bytes")

        query_performance = cls(
            seq_scan_count=seq_scan_count,
            seq_scan_rows=seq_scan_rows,
            index_scan_count=index_scan_count,
            index_scan_rows=index_scan_rows,
            temp_files_count=temp_files_count,
            temp_files_bytes=temp_files_bytes,
        )

        query_performance.additional_properties = d
        return query_performance

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
