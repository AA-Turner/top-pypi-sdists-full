from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.qa_gate_status_response_dto_all_passed_by_stage import QaGateStatusResponseDtoAllPassedByStage
  from ..models.qa_gate_status_response_dto_gates_item import QaGateStatusResponseDtoGatesItem





T = TypeVar("T", bound="QaGateStatusResponseDto")



@_attrs_define
class QaGateStatusResponseDto:
    """ Combined QA gate status for a specific problem version across all gates and stages.

        Example:
            {'gates': [{'gateId': '7dcc291b-69c1-4d5a-8b1a-5d35cc07c753', 'qaConfigId': 'd6bcc57c-7b71-4369-98da-
                ab69d9571bb9', 'qaConfigName': 'semantic-critic-review', 'blockedStage': 'submitting', 'passed': True,
                'latestScore': 0.92, 'latestGrade': 'pass', 'latestJobId': 'dff37696-37ff-4504-bb59-22d728409c7b',
                'latestJobStatus': 'completed'}], 'allPassed': True, 'allPassedByStage': {'locking': True, 'running': True,
                'submitting': True}}

        Attributes:
            gates (list[QaGateStatusResponseDtoGatesItem]): Per-gate pass/fail status for the version.
            all_passed (bool): True if every QA gate passes for the version.
            all_passed_by_stage (QaGateStatusResponseDtoAllPassedByStage): Aggregated pass status broken down by stage.
     """

    gates: list[QaGateStatusResponseDtoGatesItem]
    all_passed: bool
    all_passed_by_stage: QaGateStatusResponseDtoAllPassedByStage





    def to_dict(self) -> dict[str, Any]:
        from ..models.qa_gate_status_response_dto_all_passed_by_stage import QaGateStatusResponseDtoAllPassedByStage # noqa: PLC0415
        from ..models.qa_gate_status_response_dto_gates_item import QaGateStatusResponseDtoGatesItem # noqa: PLC0415
        gates = []
        for gates_item_data in self.gates:
            gates_item = gates_item_data.to_dict()
            gates.append(gates_item)



        all_passed = self.all_passed

        all_passed_by_stage = self.all_passed_by_stage.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "gates": gates,
            "allPassed": all_passed,
            "allPassedByStage": all_passed_by_stage,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.qa_gate_status_response_dto_all_passed_by_stage import QaGateStatusResponseDtoAllPassedByStage # noqa: PLC0415
        from ..models.qa_gate_status_response_dto_gates_item import QaGateStatusResponseDtoGatesItem # noqa: PLC0415
        d = dict(src_dict)
        gates = []
        _gates = d.pop("gates")
        for gates_item_data in (_gates):
            gates_item = QaGateStatusResponseDtoGatesItem.from_dict(gates_item_data)



            gates.append(gates_item)


        all_passed = d.pop("allPassed")

        all_passed_by_stage = QaGateStatusResponseDtoAllPassedByStage.from_dict(d.pop("allPassedByStage"))




        qa_gate_status_response_dto = cls(
            gates=gates,
            all_passed=all_passed,
            all_passed_by_stage=all_passed_by_stage,
        )

        return qa_gate_status_response_dto

