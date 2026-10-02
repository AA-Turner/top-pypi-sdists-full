from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.stage_clearance_request_body_dto_type_1_stage import StageClearanceRequestBodyDtoType1Stage






T = TypeVar("T", bound="StageClearanceRequestBodyDtoType1")



@_attrs_define
class StageClearanceRequestBodyDtoType1:
    """ Clearance request that bypasses failing QA gates with a recorded reason.

        Attributes:
            stage (StageClearanceRequestBodyDtoType1Stage): Workflow stage to clear despite failing QA gates.
            override (bool): Must be true to engage the override variant.
            override_reason (str): Human-readable justification recorded with the override.
     """

    stage: StageClearanceRequestBodyDtoType1Stage
    override: bool
    override_reason: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        stage = self.stage.value

        override = self.override

        override_reason = self.override_reason


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "stage": stage,
            "override": override,
            "overrideReason": override_reason,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        stage = StageClearanceRequestBodyDtoType1Stage(d.pop("stage"))




        override = d.pop("override")

        override_reason = d.pop("overrideReason")

        stage_clearance_request_body_dto_type_1 = cls(
            stage=stage,
            override=override,
            override_reason=override_reason,
        )


        stage_clearance_request_body_dto_type_1.additional_properties = d
        return stage_clearance_request_body_dto_type_1

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
