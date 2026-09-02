from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offboard_workspace_user_response_200_summary import OffboardWorkspaceUserResponse200Summary


T = TypeVar("T", bound="OffboardWorkspaceUserResponse200")


@_attrs_define
class OffboardWorkspaceUserResponse200:
    """
    Attributes:
        conflicts (Union[Unset, List[str]]): List of path conflicts that block the offboarding. Empty on success.
        summary (Union[Unset, OffboardWorkspaceUserResponse200Summary]):
    """

    conflicts: Union[Unset, List[str]] = UNSET
    summary: Union[Unset, "OffboardWorkspaceUserResponse200Summary"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        conflicts: Union[Unset, List[str]] = UNSET
        if not isinstance(self.conflicts, Unset):
            conflicts = self.conflicts

        summary: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.summary, Unset):
            summary = self.summary.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if conflicts is not UNSET:
            field_dict["conflicts"] = conflicts
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.offboard_workspace_user_response_200_summary import OffboardWorkspaceUserResponse200Summary

        d = src_dict.copy()
        conflicts = cast(List[str], d.pop("conflicts", UNSET))

        _summary = d.pop("summary", UNSET)
        summary: Union[Unset, OffboardWorkspaceUserResponse200Summary]
        if isinstance(_summary, Unset):
            summary = UNSET
        else:
            summary = OffboardWorkspaceUserResponse200Summary.from_dict(_summary)

        offboard_workspace_user_response_200 = cls(
            conflicts=conflicts,
            summary=summary,
        )

        offboard_workspace_user_response_200.additional_properties = d
        return offboard_workspace_user_response_200

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
