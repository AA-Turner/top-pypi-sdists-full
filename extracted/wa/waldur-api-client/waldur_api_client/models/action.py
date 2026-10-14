from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Action")


@_attrs_define
class Action:
    """
    Attributes:
        type_ (str):
        description (str):
        automatic (Union[Unset, bool]):  Default: False.
        deadline (Union[None, Unset, str]):
    """

    type_: str
    description: str
    automatic: Union[Unset, bool] = False
    deadline: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        description = self.description

        automatic = self.automatic

        deadline: Union[None, Unset, str]
        if isinstance(self.deadline, Unset):
            deadline = UNSET
        else:
            deadline = self.deadline

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "description": description,
            }
        )
        if automatic is not UNSET:
            field_dict["automatic"] = automatic
        if deadline is not UNSET:
            field_dict["deadline"] = deadline

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        description = d.pop("description")

        automatic = d.pop("automatic", UNSET)

        def _parse_deadline(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deadline = _parse_deadline(d.pop("deadline", UNSET))

        action = cls(
            type_=type_,
            description=description,
            automatic=automatic,
            deadline=deadline,
        )

        action.additional_properties = d
        return action

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
