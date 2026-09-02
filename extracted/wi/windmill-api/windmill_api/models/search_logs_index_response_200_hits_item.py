import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.search_logs_index_response_200_hits_item_level import SearchLogsIndexResponse200HitsItemLevel
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchLogsIndexResponse200HitsItem")


@_attrs_define
class SearchLogsIndexResponse200HitsItem:
    """
    Attributes:
        ts (datetime.datetime): timestamp of the log line itself, not of the file containing it
        host (str):
        level (SearchLogsIndexResponse200HitsItemLevel):
        message (str):
        file_path (str): the log file the line came from
        line_no (int): offset of the line within its file
        target (Union[Unset, None, str]): the tracing target that emitted the line
    """

    ts: datetime.datetime
    host: str
    level: SearchLogsIndexResponse200HitsItemLevel
    message: str
    file_path: str
    line_no: int
    target: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        ts = self.ts.isoformat()

        host = self.host
        level = self.level.value

        message = self.message
        file_path = self.file_path
        line_no = self.line_no
        target = self.target

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ts": ts,
                "host": host,
                "level": level,
                "message": message,
                "file_path": file_path,
                "line_no": line_no,
            }
        )
        if target is not UNSET:
            field_dict["target"] = target

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ts = isoparse(d.pop("ts"))

        host = d.pop("host")

        level = SearchLogsIndexResponse200HitsItemLevel(d.pop("level"))

        message = d.pop("message")

        file_path = d.pop("file_path")

        line_no = d.pop("line_no")

        target = d.pop("target", UNSET)

        search_logs_index_response_200_hits_item = cls(
            ts=ts,
            host=host,
            level=level,
            message=message,
            file_path=file_path,
            line_no=line_no,
            target=target,
        )

        search_logs_index_response_200_hits_item.additional_properties = d
        return search_logs_index_response_200_hits_item

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
