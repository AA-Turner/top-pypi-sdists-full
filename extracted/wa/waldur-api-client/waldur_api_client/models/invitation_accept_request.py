from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.self_declared_conflict_request import SelfDeclaredConflictRequest


T = TypeVar("T", bound="InvitationAcceptRequest")


@_attrs_define
class InvitationAcceptRequest:
    """
    Attributes:
        declared_conflicts (Union[Unset, list['SelfDeclaredConflictRequest']]): Optional list of self-declared conflicts
            with proposals. Each conflict creates a ConflictOfInterest record with detection_method='self_disclosed'.
    """

    declared_conflicts: Union[Unset, list["SelfDeclaredConflictRequest"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        declared_conflicts: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.declared_conflicts, Unset):
            declared_conflicts = []
            for declared_conflicts_item_data in self.declared_conflicts:
                declared_conflicts_item = declared_conflicts_item_data.to_dict()
                declared_conflicts.append(declared_conflicts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if declared_conflicts is not UNSET:
            field_dict["declared_conflicts"] = declared_conflicts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.self_declared_conflict_request import SelfDeclaredConflictRequest

        d = dict(src_dict)
        declared_conflicts = []
        _declared_conflicts = d.pop("declared_conflicts", UNSET)
        for declared_conflicts_item_data in _declared_conflicts or []:
            declared_conflicts_item = SelfDeclaredConflictRequest.from_dict(declared_conflicts_item_data)

            declared_conflicts.append(declared_conflicts_item)

        invitation_accept_request = cls(
            declared_conflicts=declared_conflicts,
        )

        invitation_accept_request.additional_properties = d
        return invitation_accept_request

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
