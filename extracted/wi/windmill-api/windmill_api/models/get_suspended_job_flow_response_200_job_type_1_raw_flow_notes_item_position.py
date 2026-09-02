from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetSuspendedJobFlowResponse200JobType1RawFlowNotesItemPosition")


@_attrs_define
class GetSuspendedJobFlowResponse200JobType1RawFlowNotesItemPosition:
    """Position of the note in the flow editor

    Attributes:
        x (float): X coordinate
        y (float): Y coordinate
    """

    x: float
    y: float
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        x = self.x
        y = self.y

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "x": x,
                "y": y,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        x = d.pop("x")

        y = d.pop("y")

        get_suspended_job_flow_response_200_job_type_1_raw_flow_notes_item_position = cls(
            x=x,
            y=y,
        )

        get_suspended_job_flow_response_200_job_type_1_raw_flow_notes_item_position.additional_properties = d
        return get_suspended_job_flow_response_200_job_type_1_raw_flow_notes_item_position

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
