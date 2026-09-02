from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ScorerDefaultsResponse200")


@_attrs_define
class ScorerDefaultsResponse200:
    """
    Attributes:
        judge_prompt (str): The system prompt a judge agent is created with.
        script_template (str):
    """

    judge_prompt: str
    script_template: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        judge_prompt = self.judge_prompt
        script_template = self.script_template

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "judge_prompt": judge_prompt,
                "script_template": script_template,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        judge_prompt = d.pop("judge_prompt")

        script_template = d.pop("script_template")

        scorer_defaults_response_200 = cls(
            judge_prompt=judge_prompt,
            script_template=script_template,
        )

        scorer_defaults_response_200.additional_properties = d
        return scorer_defaults_response_200

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
