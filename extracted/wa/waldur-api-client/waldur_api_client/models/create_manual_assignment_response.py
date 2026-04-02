from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.create_manual_assignment_response_skipped_proposals_item import (
        CreateManualAssignmentResponseSkippedProposalsItem,
    )


T = TypeVar("T", bound="CreateManualAssignmentResponse")


@_attrs_define
class CreateManualAssignmentResponse:
    """
    Attributes:
        batch_uuid (UUID):
        items_created (int):
        skipped_proposals (list['CreateManualAssignmentResponseSkippedProposalsItem']): Proposals that were skipped with
            reasons
    """

    batch_uuid: UUID
    items_created: int
    skipped_proposals: list["CreateManualAssignmentResponseSkippedProposalsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        batch_uuid = str(self.batch_uuid)

        items_created = self.items_created

        skipped_proposals = []
        for skipped_proposals_item_data in self.skipped_proposals:
            skipped_proposals_item = skipped_proposals_item_data.to_dict()
            skipped_proposals.append(skipped_proposals_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "batch_uuid": batch_uuid,
                "items_created": items_created,
                "skipped_proposals": skipped_proposals,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_manual_assignment_response_skipped_proposals_item import (
            CreateManualAssignmentResponseSkippedProposalsItem,
        )

        d = dict(src_dict)
        batch_uuid = UUID(d.pop("batch_uuid"))

        items_created = d.pop("items_created")

        skipped_proposals = []
        _skipped_proposals = d.pop("skipped_proposals")
        for skipped_proposals_item_data in _skipped_proposals:
            skipped_proposals_item = CreateManualAssignmentResponseSkippedProposalsItem.from_dict(
                skipped_proposals_item_data
            )

            skipped_proposals.append(skipped_proposals_item)

        create_manual_assignment_response = cls(
            batch_uuid=batch_uuid,
            items_created=items_created,
            skipped_proposals=skipped_proposals,
        )

        create_manual_assignment_response.additional_properties = d
        return create_manual_assignment_response

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
