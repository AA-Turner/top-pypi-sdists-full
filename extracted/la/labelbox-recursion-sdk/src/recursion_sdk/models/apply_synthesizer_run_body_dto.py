from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.apply_synthesizer_run_body_dto_approved_targets_item import ApplySynthesizerRunBodyDtoApprovedTargetsItem
from typing import cast






T = TypeVar("T", bound="ApplySynthesizerRunBodyDto")



@_attrs_define
class ApplySynthesizerRunBodyDto:
    """ Payload for applying an approved subset of a completed synthesizer run's diff back onto the problem version.

        Example:
            {'approvedTargets': ['prompt']}

        Attributes:
            approved_targets (list[ApplySynthesizerRunBodyDtoApprovedTargetsItem]): Subset of the diff-payload targets the
                caller approves; must be non-empty and free of duplicates.
     """

    approved_targets: list[ApplySynthesizerRunBodyDtoApprovedTargetsItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        approved_targets = []
        for approved_targets_item_data in self.approved_targets:
            approved_targets_item = approved_targets_item_data.value
            approved_targets.append(approved_targets_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "approvedTargets": approved_targets,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        approved_targets = []
        _approved_targets = d.pop("approvedTargets")
        for approved_targets_item_data in (_approved_targets):
            approved_targets_item = ApplySynthesizerRunBodyDtoApprovedTargetsItem(approved_targets_item_data)



            approved_targets.append(approved_targets_item)


        apply_synthesizer_run_body_dto = cls(
            approved_targets=approved_targets,
        )


        apply_synthesizer_run_body_dto.additional_properties = d
        return apply_synthesizer_run_body_dto

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
