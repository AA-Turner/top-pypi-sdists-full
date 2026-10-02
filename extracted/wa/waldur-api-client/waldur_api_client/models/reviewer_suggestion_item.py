from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ReviewerSuggestionItem")


@_attrs_define
class ReviewerSuggestionItem:
    """
    Attributes:
        pool_entry_uuid (UUID):
        reviewer_name (str):
        affinity_score (Union[None, float]):
        current_assignments (int):
        max_assignments (int):
    """

    pool_entry_uuid: UUID
    reviewer_name: str
    affinity_score: Union[None, float]
    current_assignments: int
    max_assignments: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pool_entry_uuid = str(self.pool_entry_uuid)

        reviewer_name = self.reviewer_name

        affinity_score: Union[None, float]
        affinity_score = self.affinity_score

        current_assignments = self.current_assignments

        max_assignments = self.max_assignments

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pool_entry_uuid": pool_entry_uuid,
                "reviewer_name": reviewer_name,
                "affinity_score": affinity_score,
                "current_assignments": current_assignments,
                "max_assignments": max_assignments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pool_entry_uuid = UUID(d.pop("pool_entry_uuid"))

        reviewer_name = d.pop("reviewer_name")

        def _parse_affinity_score(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        affinity_score = _parse_affinity_score(d.pop("affinity_score"))

        current_assignments = d.pop("current_assignments")

        max_assignments = d.pop("max_assignments")

        reviewer_suggestion_item = cls(
            pool_entry_uuid=pool_entry_uuid,
            reviewer_name=reviewer_name,
            affinity_score=affinity_score,
            current_assignments=current_assignments,
            max_assignments=max_assignments,
        )

        reviewer_suggestion_item.additional_properties = d
        return reviewer_suggestion_item

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
