import datetime
from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ListGuestsResponse200GuestsItem")


@_attrs_define
class ListGuestsResponse200GuestsItem:
    """
    Attributes:
        email (str):
        workspaces (List[str]):
        first_seen (datetime.date):
        last_seen (datetime.date):
    """

    email: str
    workspaces: List[str]
    first_seen: datetime.date
    last_seen: datetime.date
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        workspaces = self.workspaces

        first_seen = self.first_seen.isoformat()
        last_seen = self.last_seen.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "workspaces": workspaces,
                "first_seen": first_seen,
                "last_seen": last_seen,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

        workspaces = cast(List[str], d.pop("workspaces"))

        first_seen = isoparse(d.pop("first_seen")).date()

        last_seen = isoparse(d.pop("last_seen")).date()

        list_guests_response_200_guests_item = cls(
            email=email,
            workspaces=workspaces,
            first_seen=first_seen,
            last_seen=last_seen,
        )

        list_guests_response_200_guests_item.additional_properties = d
        return list_guests_response_200_guests_item

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
