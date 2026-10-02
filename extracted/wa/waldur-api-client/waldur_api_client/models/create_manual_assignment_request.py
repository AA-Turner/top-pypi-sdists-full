from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateManualAssignmentRequest")


@_attrs_define
class CreateManualAssignmentRequest:
    """
    Attributes:
        reviewer_pool_entry_uuid (UUID): UUID of the reviewer pool entry to assign proposals to
        proposal_uuids (list[UUID]): List of proposal UUIDs to assign to the reviewer
        manager_notes (Union[Unset, str]): Optional notes about this assignment
    """

    reviewer_pool_entry_uuid: UUID
    proposal_uuids: list[UUID]
    manager_notes: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reviewer_pool_entry_uuid = str(self.reviewer_pool_entry_uuid)

        proposal_uuids = []
        for proposal_uuids_item_data in self.proposal_uuids:
            proposal_uuids_item = str(proposal_uuids_item_data)
            proposal_uuids.append(proposal_uuids_item)

        manager_notes = self.manager_notes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reviewer_pool_entry_uuid": reviewer_pool_entry_uuid,
                "proposal_uuids": proposal_uuids,
            }
        )
        if manager_notes is not UNSET:
            field_dict["manager_notes"] = manager_notes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reviewer_pool_entry_uuid = UUID(d.pop("reviewer_pool_entry_uuid"))

        proposal_uuids = []
        _proposal_uuids = d.pop("proposal_uuids")
        for proposal_uuids_item_data in _proposal_uuids:
            proposal_uuids_item = UUID(proposal_uuids_item_data)

            proposal_uuids.append(proposal_uuids_item)

        manager_notes = d.pop("manager_notes", UNSET)

        create_manual_assignment_request = cls(
            reviewer_pool_entry_uuid=reviewer_pool_entry_uuid,
            proposal_uuids=proposal_uuids,
            manager_notes=manager_notes,
        )

        create_manual_assignment_request.additional_properties = d
        return create_manual_assignment_request

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
