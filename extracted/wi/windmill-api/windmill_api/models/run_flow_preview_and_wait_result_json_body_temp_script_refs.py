from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RunFlowPreviewAndWaitResultJsonBodyTempScriptRefs")


@_attrs_define
class RunFlowPreviewAndWaitResultJsonBodyTempScriptRefs:
    """Map of relative-import script path -> temp storage hash, propagated to each flow step so inline-script relative
    imports resolve from not-yet-deployed local content instead of the deployed script

    """

    additional_properties: Dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        run_flow_preview_and_wait_result_json_body_temp_script_refs = cls()

        run_flow_preview_and_wait_result_json_body_temp_script_refs.additional_properties = d
        return run_flow_preview_and_wait_result_json_body_temp_script_refs

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
