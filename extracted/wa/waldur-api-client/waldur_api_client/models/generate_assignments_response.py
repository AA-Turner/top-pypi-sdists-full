from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.generate_assignments_response_skipped_proposals_item import (
        GenerateAssignmentsResponseSkippedProposalsItem,
    )


T = TypeVar("T", bound="GenerateAssignmentsResponse")


@_attrs_define
class GenerateAssignmentsResponse:
    """
    Attributes:
        batches_created (int):
        items_created (int):
        proposals_processed (int):
        skipped_proposals (list['GenerateAssignmentsResponseSkippedProposalsItem']): Proposals that were skipped with
            reasons
    """

    batches_created: int
    items_created: int
    proposals_processed: int
    skipped_proposals: list["GenerateAssignmentsResponseSkippedProposalsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        batches_created = self.batches_created

        items_created = self.items_created

        proposals_processed = self.proposals_processed

        skipped_proposals = []
        for skipped_proposals_item_data in self.skipped_proposals:
            skipped_proposals_item = skipped_proposals_item_data.to_dict()
            skipped_proposals.append(skipped_proposals_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "batches_created": batches_created,
                "items_created": items_created,
                "proposals_processed": proposals_processed,
                "skipped_proposals": skipped_proposals,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.generate_assignments_response_skipped_proposals_item import (
            GenerateAssignmentsResponseSkippedProposalsItem,
        )

        d = dict(src_dict)
        batches_created = d.pop("batches_created")

        items_created = d.pop("items_created")

        proposals_processed = d.pop("proposals_processed")

        skipped_proposals = []
        _skipped_proposals = d.pop("skipped_proposals")
        for skipped_proposals_item_data in _skipped_proposals:
            skipped_proposals_item = GenerateAssignmentsResponseSkippedProposalsItem.from_dict(
                skipped_proposals_item_data
            )

            skipped_proposals.append(skipped_proposals_item)

        generate_assignments_response = cls(
            batches_created=batches_created,
            items_created=items_created,
            proposals_processed=proposals_processed,
            skipped_proposals=skipped_proposals,
        )

        generate_assignments_response.additional_properties = d
        return generate_assignments_response

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
