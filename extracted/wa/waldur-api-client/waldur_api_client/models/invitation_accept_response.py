from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InvitationAcceptResponse")


@_attrs_define
class InvitationAcceptResponse:
    """
    Attributes:
        detail (str):
        declared_conflicts (Union[Unset, list[UUID]]): UUIDs of created conflict records
    """

    detail: str
    declared_conflicts: Union[Unset, list[UUID]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        detail = self.detail

        declared_conflicts: Union[Unset, list[str]] = UNSET
        if not isinstance(self.declared_conflicts, Unset):
            declared_conflicts = []
            for declared_conflicts_item_data in self.declared_conflicts:
                declared_conflicts_item = str(declared_conflicts_item_data)
                declared_conflicts.append(declared_conflicts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "detail": detail,
            }
        )
        if declared_conflicts is not UNSET:
            field_dict["declared_conflicts"] = declared_conflicts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        detail = d.pop("detail")

        declared_conflicts = []
        _declared_conflicts = d.pop("declared_conflicts", UNSET)
        for declared_conflicts_item_data in _declared_conflicts or []:
            declared_conflicts_item = UUID(declared_conflicts_item_data)

            declared_conflicts.append(declared_conflicts_item)

        invitation_accept_response = cls(
            detail=detail,
            declared_conflicts=declared_conflicts,
        )

        invitation_accept_response.additional_properties = d
        return invitation_accept_response

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
