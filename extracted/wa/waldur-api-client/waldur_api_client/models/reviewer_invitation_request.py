from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReviewerInvitationRequest")


@_attrs_define
class ReviewerInvitationRequest:
    """
    Attributes:
        reviewer_uuids (list[UUID]): List of reviewer profile UUIDs to invite
        max_assignments (Union[Unset, int]):  Default: 5.
        invitation_message (Union[Unset, str]): Custom message to include in invitation email
    """

    reviewer_uuids: list[UUID]
    max_assignments: Union[Unset, int] = 5
    invitation_message: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reviewer_uuids = []
        for reviewer_uuids_item_data in self.reviewer_uuids:
            reviewer_uuids_item = str(reviewer_uuids_item_data)
            reviewer_uuids.append(reviewer_uuids_item)

        max_assignments = self.max_assignments

        invitation_message = self.invitation_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reviewer_uuids": reviewer_uuids,
            }
        )
        if max_assignments is not UNSET:
            field_dict["max_assignments"] = max_assignments
        if invitation_message is not UNSET:
            field_dict["invitation_message"] = invitation_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reviewer_uuids = []
        _reviewer_uuids = d.pop("reviewer_uuids")
        for reviewer_uuids_item_data in _reviewer_uuids:
            reviewer_uuids_item = UUID(reviewer_uuids_item_data)

            reviewer_uuids.append(reviewer_uuids_item)

        max_assignments = d.pop("max_assignments", UNSET)

        invitation_message = d.pop("invitation_message", UNSET)

        reviewer_invitation_request = cls(
            reviewer_uuids=reviewer_uuids,
            max_assignments=max_assignments,
            invitation_message=invitation_message,
        )

        reviewer_invitation_request.additional_properties = d
        return reviewer_invitation_request

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
