import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListLogFilesResponse200Item")


@_attrs_define
class ListLogFilesResponse200Item:
    """
    Attributes:
        hostname (str):
        mode (str):
        log_ts (datetime.datetime):
        file_path (str):
        json_fmt (bool):
        worker_group (Union[Unset, str]):
        ok_lines (Union[Unset, int]):
        err_lines (Union[Unset, int]):
    """

    hostname: str
    mode: str
    log_ts: datetime.datetime
    file_path: str
    json_fmt: bool
    worker_group: Union[Unset, str] = UNSET
    ok_lines: Union[Unset, int] = UNSET
    err_lines: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        hostname = self.hostname
        mode = self.mode
        log_ts = self.log_ts.isoformat()

        file_path = self.file_path
        json_fmt = self.json_fmt
        worker_group = self.worker_group
        ok_lines = self.ok_lines
        err_lines = self.err_lines

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "hostname": hostname,
                "mode": mode,
                "log_ts": log_ts,
                "file_path": file_path,
                "json_fmt": json_fmt,
            }
        )
        if worker_group is not UNSET:
            field_dict["worker_group"] = worker_group
        if ok_lines is not UNSET:
            field_dict["ok_lines"] = ok_lines
        if err_lines is not UNSET:
            field_dict["err_lines"] = err_lines

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        hostname = d.pop("hostname")

        mode = d.pop("mode")

        log_ts = isoparse(d.pop("log_ts"))

        file_path = d.pop("file_path")

        json_fmt = d.pop("json_fmt")

        worker_group = d.pop("worker_group", UNSET)

        ok_lines = d.pop("ok_lines", UNSET)

        err_lines = d.pop("err_lines", UNSET)

        list_log_files_response_200_item = cls(
            hostname=hostname,
            mode=mode,
            log_ts=log_ts,
            file_path=file_path,
            json_fmt=json_fmt,
            worker_group=worker_group,
            ok_lines=ok_lines,
            err_lines=err_lines,
        )

        list_log_files_response_200_item.additional_properties = d
        return list_log_files_response_200_item

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
