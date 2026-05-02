from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExistsEmailLocalPartJsonBody")


@_attrs_define
class ExistsEmailLocalPartJsonBody:
    """
    Attributes:
        local_part (str):
        workspaced_local_part (Union[Unset, bool]):
        trigger_path (Union[Unset, str]):
    """

    local_part: str
    workspaced_local_part: Union[Unset, bool] = UNSET
    trigger_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        local_part = self.local_part
        workspaced_local_part = self.workspaced_local_part
        trigger_path = self.trigger_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "local_part": local_part,
            }
        )
        if workspaced_local_part is not UNSET:
            field_dict["workspaced_local_part"] = workspaced_local_part
        if trigger_path is not UNSET:
            field_dict["trigger_path"] = trigger_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        local_part = d.pop("local_part")

        workspaced_local_part = d.pop("workspaced_local_part", UNSET)

        trigger_path = d.pop("trigger_path", UNSET)

        exists_email_local_part_json_body = cls(
            local_part=local_part,
            workspaced_local_part=workspaced_local_part,
            trigger_path=trigger_path,
        )

        exists_email_local_part_json_body.additional_properties = d
        return exists_email_local_part_json_body

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
