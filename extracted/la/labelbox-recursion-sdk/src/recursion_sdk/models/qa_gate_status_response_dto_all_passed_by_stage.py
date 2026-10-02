from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="QaGateStatusResponseDtoAllPassedByStage")



@_attrs_define
class QaGateStatusResponseDtoAllPassedByStage:
    """ Aggregated pass status broken down by stage.

        Attributes:
            locking (bool): True if all gates guarding version locking pass.
            running (bool): True if all gates guarding new problem runs pass.
            submitting (bool): True if all gates guarding final submission pass.
     """

    locking: bool
    running: bool
    submitting: bool





    def to_dict(self) -> dict[str, Any]:
        locking = self.locking

        running = self.running

        submitting = self.submitting


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "locking": locking,
            "running": running,
            "submitting": submitting,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        locking = d.pop("locking")

        running = d.pop("running")

        submitting = d.pop("submitting")

        qa_gate_status_response_dto_all_passed_by_stage = cls(
            locking=locking,
            running=running,
            submitting=submitting,
        )

        return qa_gate_status_response_dto_all_passed_by_stage

