from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetJobResponse200Type1RawFlowNotesItemSize")


@_attrs_define
class GetJobResponse200Type1RawFlowNotesItemSize:
    """Size of the note in the flow editor

    Attributes:
        width (float): Width in pixels
        height (float): Height in pixels
    """

    width: float
    height: float
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        width = self.width
        height = self.height

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "width": width,
                "height": height,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        width = d.pop("width")

        height = d.pop("height")

        get_job_response_200_type_1_raw_flow_notes_item_size = cls(
            width=width,
            height=height,
        )

        get_job_response_200_type_1_raw_flow_notes_item_size.additional_properties = d
        return get_job_response_200_type_1_raw_flow_notes_item_size

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
