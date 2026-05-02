from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FlowGroup")


@_attrs_define
class FlowGroup:
    """A semantic group of flow modules for organizational purposes. Does not affect execution — modules remain in their
    original position in the flow. Groups provide naming and collapsibility in the editor. Members are computed
    dynamically from all nodes on paths between start_id and end_id.

        Attributes:
            start_id (str): ID of the first flow module in this group (topological entry point)
            end_id (str): ID of the last flow module in this group (topological exit point)
            summary (Union[Unset, str]): Display name for this group
            note (Union[Unset, str]): Markdown note shown below the group header
            autocollapse (Union[Unset, bool]): If true, this group is collapsed by default in the flow editor. UI hint only.
            color (Union[Unset, str]): Color for the group in the flow editor
    """

    start_id: str
    end_id: str
    summary: Union[Unset, str] = UNSET
    note: Union[Unset, str] = UNSET
    autocollapse: Union[Unset, bool] = False
    color: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        start_id = self.start_id
        end_id = self.end_id
        summary = self.summary
        note = self.note
        autocollapse = self.autocollapse
        color = self.color

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_id": start_id,
                "end_id": end_id,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary
        if note is not UNSET:
            field_dict["note"] = note
        if autocollapse is not UNSET:
            field_dict["autocollapse"] = autocollapse
        if color is not UNSET:
            field_dict["color"] = color

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start_id = d.pop("start_id")

        end_id = d.pop("end_id")

        summary = d.pop("summary", UNSET)

        note = d.pop("note", UNSET)

        autocollapse = d.pop("autocollapse", UNSET)

        color = d.pop("color", UNSET)

        flow_group = cls(
            start_id=start_id,
            end_id=end_id,
            summary=summary,
            note=note,
            autocollapse=autocollapse,
            color=color,
        )

        flow_group.additional_properties = d
        return flow_group

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
