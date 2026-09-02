from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GoogleCalendarEntry")


@_attrs_define
class GoogleCalendarEntry:
    """
    Attributes:
        id (str):
        summary (str):
        primary (Union[Unset, bool]):
    """

    id: str
    summary: str
    primary: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        summary = self.summary
        primary = self.primary

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "summary": summary,
            }
        )
        if primary is not UNSET:
            field_dict["primary"] = primary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        summary = d.pop("summary")

        primary = d.pop("primary", UNSET)

        google_calendar_entry = cls(
            id=id,
            summary=summary,
            primary=primary,
        )

        google_calendar_entry.additional_properties = d
        return google_calendar_entry

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
