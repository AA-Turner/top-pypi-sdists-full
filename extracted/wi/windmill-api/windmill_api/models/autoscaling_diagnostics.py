import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.autoscaling_diagnostics_decisions_item import AutoscalingDiagnosticsDecisionsItem


T = TypeVar("T", bound="AutoscalingDiagnostics")


@_attrs_define
class AutoscalingDiagnostics:
    """
    Attributes:
        decision_count (int):
        decisions (List['AutoscalingDiagnosticsDecisionsItem']):
        recording_until (Union[Unset, None, datetime.datetime]):
        recording_started_by (Union[Unset, None, str]):
    """

    decision_count: int
    decisions: List["AutoscalingDiagnosticsDecisionsItem"]
    recording_until: Union[Unset, None, datetime.datetime] = UNSET
    recording_started_by: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        decision_count = self.decision_count
        decisions = []
        for decisions_item_data in self.decisions:
            decisions_item = decisions_item_data.to_dict()

            decisions.append(decisions_item)

        recording_until: Union[Unset, None, str] = UNSET
        if not isinstance(self.recording_until, Unset):
            recording_until = self.recording_until.isoformat() if self.recording_until else None

        recording_started_by = self.recording_started_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "decision_count": decision_count,
                "decisions": decisions,
            }
        )
        if recording_until is not UNSET:
            field_dict["recording_until"] = recording_until
        if recording_started_by is not UNSET:
            field_dict["recording_started_by"] = recording_started_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.autoscaling_diagnostics_decisions_item import AutoscalingDiagnosticsDecisionsItem

        d = src_dict.copy()
        decision_count = d.pop("decision_count")

        decisions = []
        _decisions = d.pop("decisions")
        for decisions_item_data in _decisions:
            decisions_item = AutoscalingDiagnosticsDecisionsItem.from_dict(decisions_item_data)

            decisions.append(decisions_item)

        _recording_until = d.pop("recording_until", UNSET)
        recording_until: Union[Unset, None, datetime.datetime]
        if _recording_until is None:
            recording_until = None
        elif isinstance(_recording_until, Unset):
            recording_until = UNSET
        else:
            recording_until = isoparse(_recording_until)

        recording_started_by = d.pop("recording_started_by", UNSET)

        autoscaling_diagnostics = cls(
            decision_count=decision_count,
            decisions=decisions,
            recording_until=recording_until,
            recording_started_by=recording_started_by,
        )

        autoscaling_diagnostics.additional_properties = d
        return autoscaling_diagnostics

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
