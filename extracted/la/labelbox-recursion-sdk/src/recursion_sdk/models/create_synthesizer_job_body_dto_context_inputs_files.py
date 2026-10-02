from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CreateSynthesizerJobBodyDtoContextInputsFiles")



@_attrs_define
class CreateSynthesizerJobBodyDtoContextInputsFiles:
    """ File buckets to include in the synthesizer input tarball.

        Attributes:
            problem (bool): Include the problem primary files in the input tarball.
            supporting (bool): Include supporting (read-only) files in the input tarball.
            grader_support (bool): Include grader-support files (non-gold) in the input tarball.
            gold_standard (bool): Include gold-standard files in the input tarball.
     """

    problem: bool
    supporting: bool
    grader_support: bool
    gold_standard: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        problem = self.problem

        supporting = self.supporting

        grader_support = self.grader_support

        gold_standard = self.gold_standard


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "problem": problem,
            "supporting": supporting,
            "graderSupport": grader_support,
            "goldStandard": gold_standard,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        problem = d.pop("problem")

        supporting = d.pop("supporting")

        grader_support = d.pop("graderSupport")

        gold_standard = d.pop("goldStandard")

        create_synthesizer_job_body_dto_context_inputs_files = cls(
            problem=problem,
            supporting=supporting,
            grader_support=grader_support,
            gold_standard=gold_standard,
        )


        create_synthesizer_job_body_dto_context_inputs_files.additional_properties = d
        return create_synthesizer_job_body_dto_context_inputs_files

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
