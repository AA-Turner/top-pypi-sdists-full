from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetBillableSeatsResponse200")


@_attrs_define
class GetBillableSeatsResponse200:
    """
    Attributes:
        seats (int):
        developers (Union[Unset, int]): Omitted when the seats counted are another workspace's, as they are for a fork
            resolving to its billing root.
        operators (Union[Unset, int]): Omitted when the seats counted are another workspace's, as they are for a fork
            resolving to its billing root.
    """

    seats: int
    developers: Union[Unset, int] = UNSET
    operators: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        seats = self.seats
        developers = self.developers
        operators = self.operators

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "seats": seats,
            }
        )
        if developers is not UNSET:
            field_dict["developers"] = developers
        if operators is not UNSET:
            field_dict["operators"] = operators

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        seats = d.pop("seats")

        developers = d.pop("developers", UNSET)

        operators = d.pop("operators", UNSET)

        get_billable_seats_response_200 = cls(
            seats=seats,
            developers=developers,
            operators=operators,
        )

        get_billable_seats_response_200.additional_properties = d
        return get_billable_seats_response_200

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
