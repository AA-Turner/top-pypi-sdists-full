from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SynthesizerJobDtoContextInputsFiles")



@_attrs_define
class SynthesizerJobDtoContextInputsFiles:
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





    def to_dict(self) -> dict[str, Any]:
        problem = self.problem

        supporting = self.supporting

        grader_support = self.grader_support

        gold_standard = self.gold_standard


        field_dict: dict[str, Any] = {}

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

        synthesizer_job_dto_context_inputs_files = cls(
            problem=problem,
            supporting=supporting,
            grader_support=grader_support,
            gold_standard=gold_standard,
        )

        return synthesizer_job_dto_context_inputs_files

