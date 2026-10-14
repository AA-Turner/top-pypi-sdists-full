from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.stage_enum import StageEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offering_merge_execute_report import OfferingMergeExecuteReport
    from ..models.offering_merge_undo_report import OfferingMergeUndoReport


T = TypeVar("T", bound="OfferingMergeVerification")


@_attrs_define
class OfferingMergeVerification:
    """
    Attributes:
        stage (StageEnum):
        passed (bool):
        execute (Union[Unset, OfferingMergeExecuteReport]):
        undo (Union[Unset, OfferingMergeUndoReport]):
    """

    stage: StageEnum
    passed: bool
    execute: Union[Unset, "OfferingMergeExecuteReport"] = UNSET
    undo: Union[Unset, "OfferingMergeUndoReport"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        stage = self.stage.value

        passed = self.passed

        execute: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.execute, Unset):
            execute = self.execute.to_dict()

        undo: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.undo, Unset):
            undo = self.undo.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "stage": stage,
                "passed": passed,
            }
        )
        if execute is not UNSET:
            field_dict["execute"] = execute
        if undo is not UNSET:
            field_dict["undo"] = undo

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_merge_execute_report import OfferingMergeExecuteReport
        from ..models.offering_merge_undo_report import OfferingMergeUndoReport

        d = dict(src_dict)
        stage = StageEnum(d.pop("stage"))

        passed = d.pop("passed")

        _execute = d.pop("execute", UNSET)
        execute: Union[Unset, OfferingMergeExecuteReport]
        if isinstance(_execute, Unset):
            execute = UNSET
        else:
            execute = OfferingMergeExecuteReport.from_dict(_execute)

        _undo = d.pop("undo", UNSET)
        undo: Union[Unset, OfferingMergeUndoReport]
        if isinstance(_undo, Unset):
            undo = UNSET
        else:
            undo = OfferingMergeUndoReport.from_dict(_undo)

        offering_merge_verification = cls(
            stage=stage,
            passed=passed,
            execute=execute,
            undo=undo,
        )

        offering_merge_verification.additional_properties = d
        return offering_merge_verification

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
