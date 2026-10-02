from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.stage_clearance_request_body_dto_type_0_stage import StageClearanceRequestBodyDtoType0Stage
from ..types import UNSET, Unset






T = TypeVar("T", bound="StageClearanceRequestBodyDtoType0")



@_attrs_define
class StageClearanceRequestBodyDtoType0:
    """ Clearance request that relies on passing QA gates for the given stage.

        Attributes:
            stage (StageClearanceRequestBodyDtoType0Stage): Workflow stage to clear via passing QA results.
            override (bool | Unset): Must be omitted or false in the passthrough variant.
     """

    stage: StageClearanceRequestBodyDtoType0Stage
    override: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        stage = self.stage.value

        override = self.override


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "stage": stage,
        })
        if override is not UNSET:
            field_dict["override"] = override

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        stage = StageClearanceRequestBodyDtoType0Stage(d.pop("stage"))




        override = d.pop("override", UNSET)

        stage_clearance_request_body_dto_type_0 = cls(
            stage=stage,
            override=override,
        )


        stage_clearance_request_body_dto_type_0.additional_properties = d
        return stage_clearance_request_body_dto_type_0

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
